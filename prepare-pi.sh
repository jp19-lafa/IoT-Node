#!/bin/sh

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

# perform a system update. This should be executed first
function update-system {
    apt update || exit 1
    apt upgrade -y || exit 1
}

# install and setup pigpio and pygpiod
function setup-pygpiod {
    apt install -y pigpio || exit 1
    wget https://raw.githubusercontent.com/joan2937/pigpio/master/util/pigpiod.service || exit 1
    mv pigpiod.service /etc/systemd/system || exit 1
    systemctl enable pigpiod.service || exit 1
    systemctl start pigpiod.service || exit 1
}

# enable i2c as defined in the raspi-config
function enable-i2c {
    dtparam i2c=on || exit 1
    if ! grep -q "^i2c[-_]dev" /etc/modules; then
        printf "i2c-dev\n" >> /etc/modules
    fi
    modprobe i2c-dev
}

# enable one wire as defined in the raspi-config
function enable-w1 {
    printf "dtoverlay=w1-gpio\n" >> /boot/config.txt || exit 1
}

# install all software needed to run the IoT Node
function execute {
    update-system
    enable-i2c
    enable-w1
    apt install -y python-smbus python3-smbus python-dev python3-dev i2c-tools || exit 1 # install smbus for i2c
    modprobe w1-gpio || exit 1
    setup-pygpiod || exit 1
}

# only run the commands when you are root.
if [ "$(id)" == "0" ]; then
    execute
else
    printf "You must be root to be able to modify the system"
fi
