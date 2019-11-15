import logger
import bluetooth
import subprocess

from bluetooth.ble import DiscoveryService

hostMACAddress = '' # The MAC address of a Bluetooth adapter on the server. Leave blank to use default connection
port = 3
backlog = 1
size = 1024
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def pair():
    logger.log("Trying to pair with a device", logger.LOG_DEBUG)
    subprocess.call("bluetoothctl --command power on")
    subprocess.call("bluetoothctl --command scan on")
    subprocess.call("bluetoothctl --command agent on")
    while 1:
        service = DiscoveryService()
        devices = service.discover(5)
        for address, name in devices.items():
            logger.log("Name: {}, address: {}".format(name, address), logger.LOG_DEBUG)
            try:
                subprocess.check_output("bluetoothctl --command pair {}".format(address), shell=True)
            except subprocess.CalledProcessError as e:
                continue
            try:
                subprocess.check_output("bluetoothctl --command connect {}".format(address), shell=True)
            except subprocess.CalledProcessError as e:
                continue
            return address
    return ""





def startup(server):
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)
    pair()
    server.bind((hostMACAddress, port))
    server.listen(backlog)
    return server

def idle(server):
    logger.log("Waiting for a bluetooth connection", logger.LOG_DEBUG)
    try:
        client, clientInfo = server.accept()
        
    except:	
        print("Closing socket")
        client.close()
        server.close()
    return client, clientInfo

def getWifiData(client, clientInfo, server):
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
