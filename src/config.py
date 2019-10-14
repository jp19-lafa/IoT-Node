# helper functions
from uuid import getnode as get_mac

mac = get_mac()
mac = "".join(c + ":" if i % 2 else c for i,
              c in enumerate(hex(mac)[2:].zfill(12)))[:-1]


server = "mira.systems"  # The server to connect to
user = mac  # the user to connect with mqtt
passwd = ""  # the password of said user
port = 1886    # the mqtt port
interval = 10  # how quickly to cycle through mqtt cycles
food = 22  # pin on the rpi for the food pump
pump = 27  # pin on the rpi for the water pump
light = 17  # pin on the rpi for the lights
sensorfile = "sensors.data"

subscribe = ["/actuators/lightint",
             "/actuators/flowpump", "/actuators/foodpump"]

sensors = ["/sensors/airtemp", "/sensors/watertemp",
           "/sensors/lightstr", "/sensors/airhumidity", "/sensors/waterph"]

# the moment the water level is to high (value between 0 and 255)
RISKY_WATER_LEVEL = 150
