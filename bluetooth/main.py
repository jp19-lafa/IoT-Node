import wifi
import helper

def isConnectedTOWifi():
    return wifi.ConnectedToTheNetwork()

def establishConnection():
    helper.log("Trying to establish a wifi connection over bluetooth")

def start_farm():
    helper.log("Starting farm", helper.LOG_DEBUG)
    helper.log("Starting farm", helper.LOG_WARM)
    helper.log("Starting farm", helper.LOG_ERROR)


if __name__ == "__main__":
    if isConnectedTOWifi():
        helper.log("Connected to the wifi")
        start_farm()
    establishConnection()
    start_farm()