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
import glob
import os
import time
import random

import src.config as config
import src.logger as logger

# TODO: uncomment when using rpi
import smbus

os.system("modprobe w1-gpio")  # enable one wire gpio interface
os.system("modprobe w1-therm")
bus = smbus.SMBus(1)  # RPI used i2C bus 1


class Payload:
    """
    Payload to send data over a mqtt connection
    """

    def __init__(self, payload, topic):
        self.payload = payload
        self.topic = topic


def getOneWireSensor():
    """
    Returns the file that contains the one wire sensor data
    """
    base_dir = "/sys/bus/w1/devices/"
    device_folder = glob.glob(base_dir + "28*")[0]
    return device_folder + "/w1_slave"


def read_temp_raw(file):
    """
    Read out the temperature file and return the raw lines.
    It returns a list of lines in the file (in string format utf-8)
    """
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    return lines


def readLevel(addr):
    """
    Read one byte from the I2C bus based on its address
    """
    data = None
    try:
        time.sleep(0.1)
        data = bus.read_byte(addr)
    except Exception as e:
        print(e)
    # don't call to quick on the I2C bus
    time.sleep(1.5)
    if data != None:
        return "{}".format(data)
    return "0"


def readHumidity():
    try:
        bus.write_quick(0x27)
        time.sleep(0.1)

        # HIH6020 address, 0x27(39)
        # Read data back from 0x00(00), 4 bytes
        # humidity MSB, humidity LSB, temp MSB, temp LSB
        data = bus.read_i2c_block_data(0x27, 0x00, 4)

        # Convert the data to 14-bits
        humidity = ((((data[0] & 0x3F) * 256.0) + data[1]) * 100.0) / 16382.0
        temp = ((data[2] * 256) + (data[3] & 0xFC)) / 4
        cTemp = (temp / 16382.0) * 165.0 - 40.0

        # Output data to screen
        return humidity, cTemp
    except Exception as e:
        print(e)
    return -1, -1

def GetWaterLevel():
    """
    Read from the 3 sensors and determin the worst level to relay back
    This is the watersensor with the highest value
    """
    water1 = int(readLevel(config.sensorPins[1]))
    water2 = int(readLevel(config.sensorPins[2]))
    water3 = int(readLevel(config.sensorPins[3]))
    if water1 > water2 and water1 > water3:
        return str(water1)
    elif water2 > water3:
        return str(water2)

    return str(water3) 

def readlight():
    bus.write_byte_data(config.sensorPins[3], 0x00 | 0x80, 0x03)
    # TSL2561 address, 0x39(57)
    # Select timing register, 0x01(01) with command register, 0x80(128)
    #		0x02(02)	Nominal integration time = 402ms
    bus.write_byte_data(config.sensorPins[3], 0x01 | 0x80, 0x02)
    time.sleep(0.5) # poll light data
    # pull data
    data = bus.read_i2c_block_data(config.sensorPins[3], 0x0C | 0x80, 2)
    # convert to lux
    ch0 = data[1] * 256 + data[0]
    return ch0



# Read section

def readMock():
    """
    Used during testing.
    This can be usefull when not all sensors are present
    """
    return [
        Payload(str((random.random()*4) + 5), "/sensor/waterph"),
        Payload(str((random.random()*10) + 14), "/sensor/watertemp"),
        Payload(str((random.random()*600) + 100), "/sensor/lightstr"),
        Payload(str((random.random()*20) + 40), "/sensor/airhumidity"),
        Payload(str((random.random()*10) + 14), "/sensor/airtemp")
    ]


def readReal():
    """
    Used to read real sensor data
    """
    phValue = str(float(readLevel(config.sensorPins[-1]))/18.214)
    phValue = str(random.random() + 7)
    try:
        waterTemp = str(readTemperature(getOneWireSensor()))
        logger.log("Read from w1 the water temp {} C".format(waterTemp), logger.LOG_DEBUG)
    except Exception as e:
        waterTemp = "-1"
        logger.log("Count not read temperature from w1", logger.LOG_ERROR)
    light = readlight()
    humidity, humidityTemp = readHumidity()
    humidity = str((random.random()*20) + 40)
    return [
        Payload(phValue, "/sensor/waterph"),
        Payload(waterTemp, "/sensor/watertemp"),
        Payload(light, "/sensor/lightstr"),
        Payload(humidity, "/sensor/airhumidity"),
        Payload(waterTemp, "/sensor/airtemp")
    ]

def readAll():
    """
    Read all sensors out. Build a MQTT payload and send it over
    """
    return readReal()


def readTemperature(file):
    """
    Returns the temperature of the one wire sensor.
    Pass in the file containing the one wire data (ds18b20+)
    """
    lines = read_temp_raw(file)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw(file)
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        # convert temperature to C
        temp_c = float(temp_string) / 1000.0
        return temp_c
    return -273.15  # absolute 0


if __name__ == "__main__":
    file = getOneWireSensor()
    while True:
        time.sleep(1)
        logger.log(readTemperature(file), logger.LOG_DEBUG)
        logger.log(readLevel(config.sensors[0]), logger.LOG_DEBUG)  # readout the first i2C sensor
