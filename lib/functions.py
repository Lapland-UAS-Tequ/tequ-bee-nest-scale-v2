import time
from sys import print_exception
import network


def average(lst):
    return sum(lst) / len(lst)


def create_payload(xbee_obj, openscale_data, power_sensor_data, boot_count):
    try:
        internalTempXBee = xbee_obj.atcmd('TP')
        if internalTempXBee > 0x7FFF:
            internalTempXBee = internalTempXBee - 0x10000

        data = {
            "d": {
                "1": {
                    "1": {
                        "v": float(openscale_data[1])
                    },
                    "2": {
                        "v": float(openscale_data[3])
                    },
                    "3": {
                        "v": float(openscale_data[4])
                    },
                    "4": {
                        "v": float(openscale_data[5])
                    },
                    "5": {
                        "v": int(boot_count)
                    },
                    "6": {
                        "v": internalTempXBee
                    },
                    "7": {
                        "v": xbee_obj.atcmd('%V')
                    },
                    "8": {
                        "v": power_sensor_data[0]
                    },
                    "9": {
                        "v": power_sensor_data[1]
                    },
                    "10": {
                        "v": power_sensor_data[2]
                    },

                }
            }
        }
    except Exception as e:
        log("functions.create_payload... FAILED")
        print_exception(e)
        return None
    else:
        log("functions.create_payload... OK")
        return data


def read_openscale_data(uart_obj):
    data = None
    count = 0
    good_data_count = 0
    # Cycle a few readings to get more accurate measurements
    log("functions.read_openscale_data - Reading sensor data...")
    while count < 30:
        count += 1
        data = uart_obj.readline()

        # Check if data None
        if count > 30:
            log("functions.read_openscale_data - Count over 50 return none...")
            data = None
            break
        elif data is None:
            log("functions.read_openscale_data - Data none, retrying...")
        else:
            data = data.decode().split(',')
            # Check if data good, retry if not.
            # Data is good if the split data packet has 7 elements
            # This value should be changed if the Sparkfun Openscale board's configuration is changed.
            if len(data) != 7:
                log("functions.read_openscale_data - Text or corrupted data, retrying...")
                print(data)
                data = None
            else:
                good_data_count += 1
                log("functions.read_openscale_data - Good data found %d/3" % good_data_count)
                print(data)

                if good_data_count == 3:
                    break
    return data


def log(string):
    logTime = time.localtime()
    logTime = "%02d-%02d-%02d %02d:%02d:%02d" % (
        logTime[0], logTime[1], logTime[2], logTime[3], logTime[4], logTime[5]
    )
    print("%s : %s" % (logTime, string))


def enable_secondary_uart(uart_obj, xbee_obj):
    try:
        xbee_obj.atcmd('P2', 7)
        xbee_obj.atcmd('D4', 7)
        uart_obj.init(9600, bits=8, parity=None, stop=1, timeout=1000)
    except Exception as e:
        log("functions.enable_secondary_uart - Enabling UART... FAILED")
        print_exception(e)
    else:
        log("functions.enable_secondary_uart - Enabling UART... OK")


def disable_secondary_uart(uart_obj, xbee_obj):
    try:
        uart_obj.deinit()
        xbee_obj.atcmd('P2', 0)
        xbee_obj.atcmd('D4', 0)
    except Exception as e:
        log("functions.disable_secondary_uart - Disabling UART... FAILED")
        print_exception(e)
    else:
        log("functions.disable_secondary_uart - Disabling UART... OK")


def configure_xbee(xbee_obj):
    try:
        xbee_obj.atcmd('BD', 7)
        xbee_obj.atcmd('NB', 0)
        xbee_obj.atcmd('SB', 0)
        xbee_obj.atcmd('SM', 0)
        xbee_obj.atcmd('AM', 0)
        xbee_obj.atcmd('AN', "internet")
        xbee_obj.atcmd('N#', 0)
        xbee_obj.atcmd('CP', 0)  # 0 = autodetect 1 = no profile
        xbee_obj.atcmd("BM", b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        xbee_obj.atcmd('DO', 17)
        xbee_obj.atcmd('MO', 7)
        xbee_obj.atcmd('D0', 4) # DIGITAL OUT LOW
        xbee_obj.atcmd('D1', 0)
        xbee_obj.atcmd('D2', 0)
        xbee_obj.atcmd('D3', 0)
        xbee_obj.atcmd('D4', 7)  # secondary UART TX
        xbee_obj.atcmd('D5', 1)
        xbee_obj.atcmd('D6', 0)
        xbee_obj.atcmd('D7', 0)
        xbee_obj.atcmd('D8', 0)  # SLEEP_REQUEST (IN)
        xbee_obj.atcmd('D9', 1)  # ON_SLEEP
        xbee_obj.atcmd('P0', 0)  # RSSI
        xbee_obj.atcmd('P1', 0)
        xbee_obj.atcmd('P2', 7)  # secondary UART RX
        xbee_obj.atcmd('P3', 1)  # UART DOUT
        xbee_obj.atcmd('P4', 1)  # UART DIN
        xbee_obj.atcmd('%L', 3150)
        xbee_obj.atcmd('%M', 100)
        xbee_obj.atcmd('PS', 1)
        xbee_obj.atcmd('AP', 4)
        # xbee_obj.atcmd('AP', 1)
        xbee_obj.atcmd('BT', 0)
        # xbee_obj.atcmd("PR, b'\x00')
        xbee_obj.atcmd('D1', 6)  # I2C SCL
        xbee_obj.atcmd('P1', 6)  # I2C SDA
    except Exception as e:
        log("functions.configure_xbee - Configuring XBee... FAILED")
        print_exception(e)
    else:
        log("functions.configure_xbee - Configuring XBee... OK")
