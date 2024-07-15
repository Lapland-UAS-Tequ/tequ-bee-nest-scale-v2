from umqtt.simple import MQTTClient
from machine import UART
from machine import Pin
import machine
import xbee
import time
import network
import ujson
from functions import createPayload, readData, log

log("Main: Tequ - Bee Scale v2 - [2024-07-15]")
watchdog = machine.WDT(timeout=180000, response=machine.CLEAN_SHUTDOWN)

sleepTime_ms = 3600000
cellular = network.Cellular()
cellular.active(True)
# while not cellular.isconnected():
#    log("Attempting connection...")
#    time.sleep_ms(1000)

# Sleep button currently doesn't work, since internal pull-up resistor doesn't appear to work
#wakeButton = Pin('D8', mode=Pin.IN, pull=Pin.)

# Start serial connection to Sparkfun Openscale
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout=1000)

boot_count = 0
x = xbee.XBee()

file = open('config.json')
settings = {}
settings = ujson.loads(file.read())

imei = str(x.atcmd('IM'))
client_id = imei
server_url = settings["url"]
port = int(settings["port"])
password = settings["password"]
username = imei
topic = ""

client = MQTTClient(client_id=client_id, server=server_url, port=port, user=username, password=password, keepalive=60)

while True:
    #cellular.active(True)
    log("Getting sensor data...")
    boot_count += 1
    payload = createPayload(x, readData(uart), boot_count)
    log("Sensor data got")
    payload = ujson.dumps(payload)
    log("Establishing cellular connection...")
    while not cellular.isconnected():
        log("Attempting connection...")
        time.sleep_ms(1000)
    log("Connected")
    log("Sending data...")
    client.connect()
    client.publish(topic, payload)
    log("Data sent")
    log("Sent payload: "+str(payload))
    log("Going to sleep...\n")
    watchdog.feed()
    cellular.active(False)
    sleep_ms = x.sleep_now(sleepTime_ms, False)
    log("Slept for: "+str(sleep_ms))
    if x.wake_reason() is xbee.PIN_WAKE:
        log("Woke up early on pin toggle")
    elif x.wake_reason() is xbee.RTC_WAKE:
        log("Woke up on time")
    else:
        log("Woke up somehow else")