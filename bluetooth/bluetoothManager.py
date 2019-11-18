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
    subprocess.call("bluetoothctl power on", shell=True)
    subprocess.call("bluetoothctl agent NoInputNoOutput", shell=True)
    while 1:
        subprocess.call("bluetoothctl discoverable-timeout 100", shell=True)
        subprocess.call("bluetoothctl discoverable on", shell=True)
        service = DiscoveryService()
        devices = service.discover(5)
        try:
                subprocess.check_output("bluetoothctl pair", shell=True)
                logger.log("Pairing sucesfull")
        except subprocess.CalledProcessError as e:
            print(e.stdout.decode("utf-8") )
            if("Connected: yes" in e.stdout.decode("utf-8") ):
                    subprocess.call("bluetoothctl discoverable off", shell=True)
                    for i in e.stdout.decode("utf-8") .split("\n"):
                        if("Connected: yes" in i):
                            return i.split(" ")[2]
            logger.log("Pairing failed, retrying", logger.LOG_ERROR)
            continue
        for address, name in devices.items():
            logger.log("Name: {}, address: {}".format(name, address), logger.LOG_DEBUG)
            try:
                subprocess.check_output("bluetoothctl connect {}".format(address), shell=True)
            except subprocess.CalledProcessError as e:
                if("Connected: yes" in e.stdout.decode("utf-8") ):
                    subprocess.call("bluetoothctl discoverable off", shell=True)
                    return address
                continue
            subprocess.call("bluetoothctl discoverable off", shell=True)
            return address
    subprocess.call("bluetoothctl discoverable off", shell=True)
    return ""





def startup(server):
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)
    logger.log("Connected to bluetooth device: {} ".format(pair()), logger.LOG_DEBUG)
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
