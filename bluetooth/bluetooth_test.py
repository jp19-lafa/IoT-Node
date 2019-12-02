# These unit tests won't cover everything since the bluetooth connections themselfs are more of an integration test than a unit test
import socket
import subprocess
import unittest
from time import sleep

import helper
import wifi


class TestHelperIDPersistance(unittest.TestCase):
    def test_idIsPersistant(self):
        # check that the id doesn't change after a certain timeout
        timeout = helper.unique_id()
        sleep(1)
        self.assertTrue(helper.unique_id() == timeout)

    def test_idIsPersistantInZeroTime(self):
        # check that the id doesn't get mutated
        self.assertTrue(helper.unique_id() == helper.unique_id())


class TestNetworkCheck(unittest.TestCase):
    def test_isHostConnectedToWifi(self):
        # check that the network does in fact exists
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                ("1.1.1.1", 53))
            self.assertTrue(True)
        except socket.error as ex:
            self.assertTrue(False)

    def test_IsConnectedToWifi(self):
        # check if a network connection exists
        self.assertTrue(wifi.ConnectedToTheNetwork())

    def test_IsConnectedToWifi(self):
        # check if a network connection and is in fact real
        connected = True
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                ("1.1.1.1", 53))
        except socket.error as ex:
            connected = False
        self.assertTrue(wifi.ConnectedToTheNetwork())
        self.assertTrue(connected)


class TestCommandsExists(unittest.TestCase):
    def test_bluetoothctl_exists(self):
        # check that the bluetoothclt exists
        self.assertTrue(
            subprocess.call("command -v bluetoothctl", shell=True) == 0)

    def test_wpa_supplicant_exists(self):
        # check that wpa_supplicant exists
        self.assertTrue(
            subprocess.call("command -v wpa_supplicant", shell=True) == 0)

    def test_wpa_supplicant_exists(self):
        # check if the init daemon is systemctl
        self.assertTrue(
            subprocess.call("command -v systemctl", shell=True) == 0)
