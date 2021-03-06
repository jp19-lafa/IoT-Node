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
import subprocess
import time

import pair.autopair as pairable
import pair.config as config
import pair.helper as helper
import pair.logger as logger
import pair.wifi as wifi
import pair.wpa as wpa

import bluetooth
from bluetooth.ble import DiscoveryService

# The MAC address of a Bluetooth adapter on the server. Leave blank to use default connection
hostMACAddress = ""
port = bluetooth.PORT_ANY
backlog = 1
size = 1024
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


class wifiConnection:
    def __init__(self):
        self.password = None
        self.ssid = None
        logger.log("WPA2 connection created")


    def try_connect(self):
        """
        Trying to connect to the network
        """
        logger.log("Trying to connect to the network {}".format(self.ssid))
        # TODO: try to connect to the network using the given credentials
        cli = wpa.wpa(["ssid {}".format(self.ssid), "psk {}".format(self.password)])
        cli.execute()
        # give time to connect
        time.sleep(config.WIFI_WAIT_UNTIL_CONNECTION)
        return wifi.ConnectedToTheNetwork()

class wifiMCHAPConnection:
    def __init__(self):
        self.password = None
        self.username = None
        self.ssid = None
        logger.log("MCHAP connection created")

    def try_connect(self):
        """
        Trying to connect to the network
        """
        logger.log("Trying to connect to the network {}".format(self.ssid))
        # TODO: try to connect to the network using the given credentials
        cli = wpa.wpa(["ssid {}".format(self.ssid),
        "key_mgmt WPA_EAP", "eap PEAP", "identity {}".format(self.username), "password {}".format(self.password)])
        cli.execute()
        # give time to connect
        time.sleep(config.WIFI_WAIT_UNTIL_CONNECTION)
        return wifi.ConnectedToTheNetwork()


def pair():
    """
    Function to try to pair with a phone.
    Note that this function accepts all pair request that come in
    """
    logger.log("Trying to pair with a device", logger.LOG_DEBUG)

    # only continue if there is no network
    if wifi.ConnectedToTheNetwork():
        return

    # wait unitl we pair with a devices
    AutoPair = pairable.BtAutoPair()
    logger.log("Configuring discoverability settings")
    AutoPair.enable_pairing()
    logger.log("Done configuring bluetooth settings")

    # check if we paired with a new device
    has_connected = subprocess.check_output("bluetoothctl info | head -n1",
                                            shell=True).decode("utf-8")
    logger.log(has_connected)
    while "Missing" in has_connected:
        has_connected = subprocess.check_output("bluetoothctl info | head -n1",
                                                shell=True).decode("utf-8")
        time.sleep(0.1)
    logger.log("Connected with device: " + has_connected)

    return has_connected.split(" ")[1]


def startup(server):
    """
    Initialize a bluetooth server so that we can communicate with the client phone
    @server is the bluetooth connection server
    """
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)
    logger.log("Connected to bluetooth device: {} ".format(pair()),
               logger.LOG_DEBUG)
    if wifi.ConnectedToTheNetwork():
        return
    server.bind((hostMACAddress, port))
    server.listen(backlog)
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    bluetooth.advertise_service(
        sock=server,
        name="Bluetooth Speaker",
        service_id=uuid,
        service_classes=[bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )

    return server


def idle(server):
    """
    Wait until a bluetooth connection is made
    @server is the bluetooth connection server
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
    """
    We split the payload and extract the command and value from it.
    If the command is equal to the expected command then we can return the value
    Otherwise we return a nullptr
    @command is a string containing the expected bluetooth command
    @data is the payload send over bluetooth (also a string)
    """
    split = data.replace("\r\n", "").split(":")
    if len(data) < 2:
        logger.log("Incomming data payload is to small, {}".format(split))
        return None
    if not split[0] == command:
        logger.log(
            "Extracted data doesn't match expected type, {} but got {} instead"
            .format(command, split[0]))
        return None
    logger.log(
        "Retreived data from bluetooth socker: {}".format("".join(split[1:])),
        logger.LOG_DEBUG,
    )
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

def extractUsername(data):
    """
    Retreive the password from the bluetooth connection
    Command should be as followed PWD:Your_password
    """
    return extractData("USER", data)


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
            if "TYPE:" in data:
                type = extractData("TYPE", data)
                if type == "wpa2":
                    connection = wifiConnection()
                elif type == "mchap":
                    connection = wifiMCHAPConnection()
                else:
                    client.send("ERROR:2 - Server doesn't recognize wifi type")
            if "SSID:" in data:
                if connection:
                    connection.ssid = extractSSID(data)
                else:
                    client.send("ERROR:1 - No connection specified")
            elif "PWD:" in data:
                if connection:
                    connection.password = extractPassword(data)
                else:
                    client.send("ERROR:1 - No connection specified")
            elif "USER:" in data:
                if connection:
                    if isinstance(connection, wifiMCHAPConnection):
                        connection.username = extractUsername(data)
                    else:
                        client.send("ERROR:4 cannot set property that is not part of the connection type")
                else:
                    client.send("ERROR:1 - No connection specified")
            elif "TRY:1" in data:
                if connection:
                    if connection.try_connect(
                    ):  # try to connect to the network
                        client.send("SUCCESS:1 - connected to a network")
                    else:
                        client.send("ERROR:3 - Network credentials are wrong")
                else:
                    client.send("ERROR:1 - No connection specified")
            else:
                client.send(data)  # Echo back to client


def set_name(name):
    """
    We change the bluetooth pretier name here
    """
    logger.log("Changing bluetooth name to {}".format(name))
    subprocess.call("bluetoothctl <<EOF\nsystem-alias {}\nEOF".format(name), shell=True)
    subprocess.call("bluetoothctl <<EOF\ndiscoverable-timeout 86400\nEOF", shell=True)
    subprocess.call("bluetoothctl <<EOF\ndiscoverable on\nEOF", shell=True)
    logger.log("Done setting bluetooth settings {}".format(name))



def EstablishConnection():
    # TODO: make a unique id as the farm name
    set_name(config.BLUETOOTH_NAME + helper.unique_id())
    startup(server)
    client, info = idle(server)
    getWifiData(client, info, server)
    logger.log("Established wifi data. Starting up farm now", logger.LOG_WARM)
