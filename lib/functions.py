import time

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
                    "sd": xbee.atcmd('%V')
                }
            }
        }
    }

    return data


def readData(uartObject):
    data = None
    count = 0

    # Cycle a few readings to get more accurate measurements
    log("Reading data...")
    while count < 5:
        count += 1
        data = uartObject.readline()
        # Check if data None
        if data == None:
            log("Data none, retrying...")
            count -= 1
            continue
        data = data.decode().split(',')
        # Check if data good, retry if not.
        # Data is good if the split data packet has 7 elements
        # This value should be changed if the Sparkfun Openscale board's configuration is changed.
        if len(data) != 7:
            log("Text or corrupted data, retrying...")
            print(data)
            count -= 1
    log("Good data found")

    return data


def log(string):
    logTime = time.localtime()
    logTime = "%02d-%02d-%02d %02d:%02d:%02d" % (
        logTime[0], logTime[1], logTime[2], logTime[3], logTime[4], logTime[5]
    )
    print("%s : %s" % (logTime, string))