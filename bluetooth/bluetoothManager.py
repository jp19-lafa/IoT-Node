import logger
import bluetooth

hostMACAddress = '00:1f:e1:dd:08:3d' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

def startup(server):
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)
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
