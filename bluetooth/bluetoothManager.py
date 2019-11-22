
# MIT License
# 
# Copyright (c) 2019 AP Hogeschool
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logger
import bluetooth
import subprocess
import time
import wifi
import autopair as pairable
import config

from bluetooth.ble import DiscoveryService

hostMACAddress = '' # The MAC address of a Bluetooth adapter on the server. Leave blank to use default connection
port = bluetooth.PORT_ANY
backlog = 1
size = 1024
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


class wifiConnection():
    def __init__(self):
        self.password = None
        self.ssid = None

    def try_connect(self):
        """
        Trying to connect to the network
        """
        logger.log("Trying to connect to the network {}".format(self.ssid))


def pair():
    """
    Function to try to pair with a phone.
    Note that this function accepts all pair request that come in
    """
    logger.log("Trying to pair with a device", logger.LOG_DEBUG)
    devices = subprocess.check_output("bluetoothctl paired-devices", shell=True)
    # only continue if there is no network
    if (wifi.ConnectedToTheNetwork()):
            return
    # wait unitl we pair with a devices
    AutoPair = pairable.BtAutoPair()
    AutoPair.enable_pairing()

    # check if we paired with a new device
    new_devices = devices
    while devices == new_devices:
        if (wifi.ConnectedToTheNetwork()):
            return
        new_devices = subprocess.check_output("bluetoothctl paired-devices", shell=True)
    
    # find the new device
    devices = devices.decode("utf-8").split("\n")
    new_devices = new_devices.decode("utf-8").split("\n")

    device = None # the device that is new
    # check if a entry is nor present in the old list
    for i in new_devices:
        if (not i in devices):
            logger.log("Found new device: {}".format(i))
            device = i.split("")[1] # set the device address as the return statement
    return device

def startup(server):
    """
    Initialize a bluetooth server so that we can communicate with the client phone
    """
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)
    #logger.log("Connected to bluetooth device: {} ".format(pair()), logger.LOG_DEBUG)
    if wifi.ConnectedToTheNetwork():
        return
    server.bind((hostMACAddress, port))
    server.listen(backlog)
    return server

def idle(server):
    """
    Wait until a bluetooth connection is made
    """
    logger.log("Waiting for a bluetooth connection", logger.LOG_DEBUG)
    if wifi.ConnectedToTheNetwork():
        return None, None
    try:
        client, clientInfo = server.accept()
        
    except:	
        print("Closing socket")
        client.close()
        server.close()
    return client, clientInfo


def extractData(command, data):
    split = data.replace("\r\n", "").split(":")
    if len(data) < 2:
        logger.log("Incomming data payload is to small, {}".format(split))
        return None
    if not split[0] == command:
        logger.log("Extracted data doesn't match expected type, {} but got {} instead".format(command, split[0]))
        return None
    logger.log("Retreived data from bluetooth socker: {}".format("".join(split[1:])), logger.LOG_DEBUG)
    return "".join(split[1:])

def extractSSID(data):
    """
    Retreive the network ssid from the bluetooth 
    Command should be as followed SSID:Your_ssid
    """
    return extractData("SSID", data)

def extractPassword(data):
    """
    Retreive the password from the bluetooth connection
    Command should be as followed PWD:Your_password
    """
    return extractData("PWD", data)

def getWifiData(client, clientInfo, server):
    """
    Comminicate with the phone over bluetooth to gather the wifi data here
    """
    if wifi.ConnectedToTheNetwork():
        return
    logger.log("Receiving wifi credentials", logger.LOG_DEBUG)
    connection = None
    while 1:
        data = client.recv(size).decode("utf-8")
        if data:
            if("TYPE:" in data):
                type = extractData("TYPE", data)
                if type == "wpa2":
                    connection = wifiConnection()
                else:
                    client.send("ERROR:2 - Server doesn't recognize wifi type")
            if("SSID:" in data):
                if connection:
                    connection.ssid = extractSSID(data)
                else:
                    client.send("ERROR:1 - No connection specified")
            elif("PWD:" in data):
                if connection:
                    connection.password = extractPassword(data)
                else:
                    client.send("ERROR:1 - No connection specified")

            elif("TRY:1" in data):
                if connection:
                    if (connection.try_connect()): # try to connect to the network
                        client.send("SUCCESS:1 - connected to a network")
                    else:
                        client.send("ERROR:3 - Network credentials are wrong")
                else:
                    client.send("ERROR:1 - No connection specified")
            client.send(data) # Echo back to client
 

# TODO: implement this function
def set_name(name):
    """
    We change the bluetooth pretier name here
    """
    logger.log("Changing bluetooth name to {}".format(name))


def EstablishConnection():
    set_name(config.BLUETOOTH_NAME) # TODO: make a unique id as the farm name
    startup(server)
    client, info = idle(server)
    getWifiData(client, info, server)
    logger.log("Established wifi data. Starting up farm now", logger.LOG_WARM)
