import wifi
import logger
import bluetoothManager

def isConnectedTOWifi():
    return wifi.ConnectedToTheNetwork()

def establishConnection():
    logger.log("Trying to establish a wifi connection over bluetooth")

def start_farm():
    logger.log("Starting farm", logger.LOG_DEBUG)


if __name__ == "__main__":
    if isConnectedTOWifi():
        logger.log("Connected to the wifi")
        start_farm()
    establishConnection()
    start_farm()