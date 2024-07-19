# import libraries
import machine
import xbee
import time
import network
import ujson
from umqtt.simple import MQTTClient
from functions import create_payload, read_openscale_data, log, average, enable_DCDC, disable_DCDC
from functions import configure_xbee, enable_secondary_uart, disable_secondary_uart, enable_I2C, disable_I2C
from sys import print_exception
import I2CSensors

log("Boot - Software tequ-bee-nest-scale-v2 - [2024-07-19]")
# Initialize watchdog
watchdog = machine.WDT(timeout=180000, response=machine.CLEAN_SHUTDOWN)
# Initialize cellular connection
cellular = network.Cellular()
cellular.active(True)

# Initialize XBee
x = xbee.XBee()
configure_xbee(x)

# Initialize secondary UART
uart = machine.UART(1)

# Read configuration file
try:
    file = open('config.json')
    settings = ujson.loads(file.read())
except Exception as e:
    log("Boot - Opening configuration file... FAILED")
    print_exception(e)
else:
    log("Boot - Opening configuration file... OK")
    log("Boot - Configuration: %s" % str(settings))

# Set variables
boot_count = 0
NORMAL_SLEEP_TIME_MS = int(settings["sleep_interval_ms"])
ERROR_SLEEP_TIME_MS = 60000
sleep_time_ms = NORMAL_SLEEP_TIME_MS

while 1:
    if cellular.isconnected():
        log("Boot - Cellular connected - Reading Device IMEI")
        imei = str(x.atcmd('IM'))

        if len(imei) > 5:
            break
        else:
            time.sleep(1)
    else:
        log("Boot - Waiting for cellular connection...")
        time.sleep(1)

log("Boot - Device IMEI: %s" % imei)
server_url = settings["mqtt_url"]
mqtt_port = int(settings["mqtt_port"])
pw = settings["mqtt_password"]
username = imei
topic = "tequ/type/bee-scale/id/"+imei+"/event/data"

# Initialize MQTT client
client = MQTTClient(client_id=imei, server=server_url, port=mqtt_port, user=username, password=pw, keepalive=15)
sensors = I2CSensors.I2CSensors(1)

while True:
    try:
        start_ticks = time.ticks_ms()
        log("Main - Running main loop...")
        boot_count += 1
        enable_I2C(x)
        enable_DCDC(x)
        sensors.initializeBus()
        sensors.scanBus()

        voltage = []
        current = []
        power = []

        for a in range(5):
            ina260_data = sensors.readINA260()
            voltage.append(ina260_data[0])
            current.append(ina260_data[1])
            power.append(ina260_data[2])

        power_sensor_data = [0, 0, 0]
        power_sensor_data[0] = average(voltage)
        power_sensor_data[1] = average(current)
        power_sensor_data[2] = average(power)

        disable_I2C(x)

        enable_secondary_uart(uart, x)
        openscale_data = read_openscale_data(uart)
        disable_DCDC(x)
        disable_secondary_uart(uart, x)
        cellular.active(True)

        while 1:
            if cellular.isconnected():
                log("Main - Cellular connected")

                if openscale_data is None:
                    log("Main - Sparkfun OpenScale sensor not working or not connected")
                    break
                else:
                    try:
                        payload = ujson.dumps(create_payload(x, openscale_data, power_sensor_data, boot_count))
                        log("Main - Connecting to MQTT server...")
                        client.connect()
                        client.publish(topic, payload)
                        log("Main - Sending data %s to MQTT server...OK" % payload)
                        sleep_time_ms = NORMAL_SLEEP_TIME_MS
                    except Exception as e:
                        log("Main - Processing sensor data... FAILED")
                        sleep_time_ms = ERROR_SLEEP_TIME_MS
                        print_exception(e)
                    finally:
                        break
            else:
                log("Main - Waiting for cellular connection...")
                time.sleep(1)
    except Exception as e:
        log("Main - Error in main loop...")
        sleep_time_ms = ERROR_SLEEP_TIME_MS
        print_exception(e)
    finally:
        log("Main - Going to sleep for %d ms..." % sleep_time_ms)
        disable_secondary_uart(uart, x)
        disable_DCDC(x)
        disable_I2C(x)
        cellular.active(False)
        end_ticks = time.ticks_ms()
        log("Main - Running main loop took: %.3f seconds" % (time.ticks_diff(end_ticks, start_ticks) / 1000))
        sleep_ms = x.sleep_now(sleep_time_ms, False)
        log("Main - Slept %d ms, wake reason: %s" % (sleep_ms, x.wake_reason()))