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
# helper functions
from uuid import getnode as get_mac

mac = get_mac()
mac = "".join(c + ":" if i % 2 else c for i, c in enumerate(hex(mac)[2:].zfill(12)))[
    :-1
]
if mac[-1:] == ":":
    mac = mac[:-1]  # in case the mac address ends with :L

server = "mira.systems"  # The server to connect to
user = mac  # the user to connect with mqtt
passwd = ""  # the password of said user
port = 1886  # the mqtt port
interval = 10  # how quickly to cycle through mqtt cycles
food = 22  # pin on the rpi for the food pump
pump = 27  # pin on the rpi for the water pump
light = 17  # pin on the rpi for the lights
sensorfile = "sensors.data"

subscribe = ["/actuators/lightint", "/actuators/flowpump", "/actuators/foodpump"]

sensors = [
    "/sensors/waterph",
    "/sensors/watertemp",
    "/sensors/lightstr",
    "/sensors/airhumidity",
    "/sensors/airtemp",
]

# list of all sensors
# Water1, Water2, Water3, light, ph
sensorPins = [0x1F, 0x20, 0x21, 0x29, 0x33]

# the moment the water level is to high (value between 0 and 255)
RISKY_WATER_LEVEL = 150
