#!/bin/bash

bluetoothctl <<EOF
power on
discoverable on
pairable on
agent NoInputNoOutput
default-agent
EOF
sleep 1
yes yes | bluetoothctl pair
