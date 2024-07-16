import time
from sys import print_exception
import network

def createPayload(xbee, sensor_values, boot_count):
    # Get current time
    #timestamp = time.localtime()

    internalTempXBee = xbee.atcmd('TP')
    if internalTempXBee > 0x7FFF:
        internalTempXBee = internalTempXBee - 0x10000

    data = {
        "d": {
            "1": {
                "1": {
                    "v": float(sensor_values[1])
                },
                "2": {
                    "v": float(sensor_values[3])
                },
                "3": {
                    "v": float(sensor_values[4])
                },
                "4": {
                    "v": float(sensor_values[5])
                },
                "5": {
                    "v": int(boot_count)
                },
                "6": {
                    "v": internalTempXBee
                },
                "7": {
                    "v": xbee.atcmd('%V')
                }
            }
        }
    }

    return data


def readData(uartObject):
    data = None
    count = 0

    # Cycle a few readings to get more accurate measurements
    log("Reading sensor data...")
    while count < 30:
        count += 1
        data = uartObject.readline()

        # Check if data None
        if count > 30:
            log("Count over 30 return none...")
            data = None
        elif data is None:
            log("Data none, retrying...")
        else:
            data = data.decode().split(',')
            # Check if data good, retry if not.
            # Data is good if the split data packet has 7 elements
            # This value should be changed if the Sparkfun Openscale board's configuration is changed.
            if len(data) != 7:
                log("Text or corrupted data, retrying...")
                print(data)
            else:
                log("Good data found")
                print(data)
                break

    return data


def log(string):
    logTime = time.localtime()
    logTime = "%02d-%02d-%02d %02d:%02d:%02d" % (
        logTime[0], logTime[1], logTime[2], logTime[3], logTime[4], logTime[5]
    )
    print("%s : %s" % (logTime, string))


def configure_xbee(xbeeObj):
    try:
        xbeeObj.atcmd('BD', 7)
        xbeeObj.atcmd('NB', 0)
        xbeeObj.atcmd('SB', 0)
        xbeeObj.atcmd('SM', 0)
        xbeeObj.atcmd('AM', 0)
        xbeeObj.atcmd('AN', "internet")
        xbeeObj.atcmd('N#', 0)
        xbeeObj.atcmd('CP', 0)  # 0 = autodetect 1 = no profile
        xbeeObj.atcmd("BM", b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        xbeeObj.atcmd('DO', 17)
        xbeeObj.atcmd('MO', 7)
        xbeeObj.atcmd('D0', 0)
        xbeeObj.atcmd('D1', 0)
        xbeeObj.atcmd('D2', 0)
        xbeeObj.atcmd('D3', 2)
        xbeeObj.atcmd('D4', 7)  # secondary UART TX
        xbeeObj.atcmd('D5', 1)
        xbeeObj.atcmd('D6', 0)
        xbeeObj.atcmd('D7', 4)
        xbeeObj.atcmd('D8', 0)  # SLEEP_REQUEST (IN)
        xbeeObj.atcmd('D9', 1)
        xbeeObj.atcmd('P0', 1)
        xbeeObj.atcmd('P1', 0)
        xbeeObj.atcmd('P2', 7)  # secondary UART RX
        xbeeObj.atcmd('P3', 1)
        xbeeObj.atcmd('P4', 1)
        xbeeObj.atcmd('%L', 3150)
        xbeeObj.atcmd('%M', 100)
        xbeeObj.atcmd('PS', 1)
        xbeeObj.atcmd('AP', 4)
        log("Configuring XBee... OK")
    except Exception as e:
        log("Configuring XBee... FAILED")
        print_exception(e)
