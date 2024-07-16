# import libraries
import machine
import xbee
import time
import network
import ujson
from umqtt.simple import MQTTClient
from functions import createPayload, readData, log, configure_xbee
from sys import print_exception

boot_count = 0
log("Main: Tequ - Bee Scale - [2024-07-16]")
log("Configuring watchdog...")
watchdog = machine.WDT(timeout=120000, response=machine.CLEAN_SHUTDOWN)

# Initialize cellular connection
cellular = network.Cellular()
cellular.active(True)

# Initialize XBee
x = xbee.XBee()
configure_xbee(x)

# Start serial connection to Sparkfun Openscale
log("Opening serial connection to SparkFun OpenScale...")
uart = machine.UART(1, 9600)

# Read configuration file
try:
    file = open('config.json')
    settings = {}
    settings = ujson.loads(file.read())
    log("Opening configuration file... OK")
except Exception as e:
    log("Opening configuration file... FAILED")
    print_exception(e)

# Set variables
sleep_time_ms = int(settings["sleep_interval_ms"])
imei = str(x.atcmd('IM'))
client_id = imei
server_url = settings["mqtt_url"]
port = int(settings["mqtt_port"])
password = settings["mqtt_password"]
username = imei
topic = "tequ/type/bee-scale/id/"+imei+"/event/data"

# Initialize MQTT client
client = MQTTClient(client_id=client_id, server=server_url, port=port, user=username, password=password, keepalive=15)

while True:
    try:
        boot_count += 1
        if not cellular.active():
            log("Enable cellular connection")
            cellular.active(True)

        # Enable second UART connection
        x.atcmd('P2', 7)
        x.atcmd('D4', 7)
        uart.init(9600, bits=8, parity=None, stop=1, timeout=1000)
        data = readData(uart)

        while 1:
            if cellular.isconnected():
                log("Cellular connected")

                if data is None:
                    log("Sparkfun OpenScale sensor not working or not connected")
                else:
                    try:
                        payload = ujson.dumps(createPayload(x, data, boot_count))
                        log("Data packet created: %s " % str(payload))
                        log("Connecting to MQTT server...")
                        client.connect()
                        client.publish(topic, payload)
                        log("Sending data to MQTT server...OK")
                        log("Sent payload: %s" % payload)
                    except Exception as e:
                        log("Processing sensor data... FAILED")
                        print_exception(e)
                    finally:
                        break
            else:
                log("Waiting for cellular connection...")

        watchdog.feed()

    finally:
        log("Going to sleep for %d ms..." % sleep_time_ms)
        # Disable second UART connection
        uart.deinit()
        x.atcmd('P2', 0)
        x.atcmd('D4', 0)
        cellular.active(False)
        sleep_ms = x.sleep_now(sleep_time_ms, False)
        log("Slept %d ms, wake reason: %s" % (sleep_ms, x.wake_reason()))