import logger
import bluetooth
import subprocess
import time
import wifi
import autopair as pairable

from bluetooth.ble import DiscoveryService

hostMACAddress = '' # The MAC address of a Bluetooth adapter on the server. Leave blank to use default connection
port = 3
backlog = 1
size = 1024
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def pair():
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
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)
    logger.log("Connected to bluetooth device: {} ".format(pair()), logger.LOG_DEBUG)
    if wifi.ConnectedToTheNetwork():
        return
    server.bind((hostMACAddress, port))
    server.listen(backlog)
    return server

def idle(server):
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

def getWifiData(client, clientInfo, server):
    if wifi.ConnectedToTheNetwork():
        return
    logger.log("Receiving wifi credentials", logger.LOG_DEBUG)
    try:
        client, clientInfo = server.accept()
        while 1:
            data = client.recv(size)
            if data:
                logger.log(data)
                client.send(data) # Echo back to client
    except:	
        print("Closing socket")
        client.close()
        server.close()

def EstablishConnection():
    startup(server)
    client, info = idle(server)
    getWifiData(client, info, server)
    logger.log("Established wifi data. Starting up farm now", logger.LOG_WARM)
