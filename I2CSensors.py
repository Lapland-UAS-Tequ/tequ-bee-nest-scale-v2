from machine import I2C
from lib.ina260 import INA260
from sys import print_exception
from utime import sleep_ms
from functions import log


class I2CSensors:
    def __init__(self, bus_number=1):
        log("I2CSensors: Initializing...")
        self.bus_number = bus_number
        self.sensors_in_bus = []
        self.bus = None
        self.led_blink_time = 100
        # self.initializeBus()
        sleep_ms(250)
        # self.scanBus()

    def initializeBus(self):
        log("I2CSensors: Initializing I2C bus...")
        self.bus = I2C(self.bus_number, freq=400000)

    def scanBus(self):
        log("I2CSensors: Scanning I2C bus...")
        self.sensors_in_bus = self.bus.scan()
        log(self.sensors_in_bus)


    def readINA260(self):
        if 64 in self.sensors_in_bus:
            try:
                ina = INA260(self.bus)
                #ina.configure()
                log("I2CSensors.readINA260: Bus Voltage: %.3f V" % ina.voltage())
                log("I2CSensors.readINA260: Current: %.3f A" % ina.current())
                log("I2CSensors.readINA260: Power: %.3f W" % ina.power())
            except Exception as e:
                print_exception(e)
                log("I2CSensors.readINA260: Reading sensor failed...")
                #blinkLED("red",self.led_blink_time ,1)
                return None
            else:
                #blinkLED("green",self.led_blink_time ,1)
                return [ina.voltage(), ina.current(), ina.power()]
        else:
            log("I2CSensors.readINA260: Sensor is not detected in the I2C bus.")
            return None
