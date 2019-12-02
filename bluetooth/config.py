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
NETWORK_CHECK = "1.1.1.1"  # url to check if the network is live
NETWORK_PORT = 53  # The port to check the network connection on
NETWORK_TIMEOUT = 1
DEBUG = True  # enable debugging messages
LOG_LEVEL = (
    3
)  # if the value is 3 print WARM, DEBUG and ERROR messages, If it is 2 only print Warn and ERROR if it is any other number print only error
BLUETOOTH_NAME = "FARMLAB-"  # A unique id will be put behind this
# timeout before people no longer can connect over bluetooth
DISCOVERABLE_TIMEOUT = 86400
