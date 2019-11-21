#!/bin/bash

bluetoothctl --agent NoInputNoOutput <<EOF
power on
discoverable on
pairable on
EOF
bluetoothctl --agent NoInputNoOutput scan on &
sleep 5
killall bluetoothctl
bluetoothctl --agent NoInputNoOutput pair BC:A5:8B:10:71:19 


