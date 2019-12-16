
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
import pair.wifi as wifi
import pair.logger as logger
import pair.bluetoothManager as bluetoothManager

def isConnectedTOWifi():
    return wifi.ConnectedToTheNetwork()

def establishConnection():
    bluetoothManager.EstablishConnection()

def start_farm():
    logger.log("Starting farm", logger.LOG_DEBUG)

def startup():
    if isConnectedTOWifi():
        logger.log("Connected to the wifi")
        start_farm()
    establishConnection()
    start_farm()

if __name__ == "__main__":
    startup()
