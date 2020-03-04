#!/bin/bash

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

# TODO: Install IoT-Node software and add a systemctl service for it

# perform a system update. This should be executed first
function updatesystem() {
  apt update || exit 1
  apt upgrade -y || exit 1
}

# install and setup pigpio and pygpiod
function setuppygpiod() {
  apt install -y pigpio || exit 1
  wget https://raw.githubusercontent.com/joan2937/pigpio/master/util/pigpiod.service || exit 1
  mv pigpiod.service /etc/systemd/system || exit 1
  systemctl enable pigpiod.service || exit 1
  systemctl start pigpiod.service || exit 1
  pip3 install pigpio
}

# enable i2c as defined in the raspi-config
function enablei2c() {
  dtparam i2c=on || exit 1
  if ! grep -q "^i2c[-_]dev" /etc/modules; then
    printf "i2c-dev\n" >>/etc/modules
  fi
  modprobe i2c-dev
}

# enable one wire as defined in the raspi-config
function enablew1() {
  printf "dtoverlay=w1-gpio\n" >>/boot/config.txt || exit 1
}

function installgattlib {
  pip3 download gattlib
  tar xvzf ./gattlib-*.tar.gz
  cd gattlib-0.20150805/
  sed -ie 's/boost_python-py34/boost_python-py35/' setup.py
  pip3 install .
}

function preparebluetooth {
  sed -i 's:ExecStart=/usr/lib/bluetooth/bluetoothd:ExecStart=/usr/lib/bluetooth/bluetoothd -C:' /etc/systemd/system/dbus-org.bluez.service
  sdptool add SP
}

# install all software needed to run the IoT Node
function execute() {
  updatesystem
  enablei2c
  enablew1
  preparebluetooth
  apt install -y python-smbus python3-smbus python-dev python3-dev i2c-tools libbluetooth-dev python-dev mercurial libglib2.0-dev libboost-python-dev libboost-all-dev libboost-thread-dev python3-pip || exit 1 # install smbus for i2c
  modprobe w1-gpio || exit 1
  setuppygpiod || exit 1
  installgattlib
  pip3 install PyBluez  pexpect # install bluetooth support
}

# only run the commands when you are root.
if [ "$(id -u)" == "0" ]; then
  execute
else
  printf "You must be root to be able to modify the system"
fi
