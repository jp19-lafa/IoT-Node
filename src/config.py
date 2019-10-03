server = "mqtt.farmlab.team"  # The server to connect to
user = "Farm"  # the user to connect with mqtt
passwd = "Lab"  # the password of said user
port = 1883  # the mqtt port
interval = 10  # how quickly to cycle through mqtt cycles
food = 22  # pin on the rpi for the food pump
pump = 27  # pin on the rpi for the water pump
light = 17  # pin on the rpi for the lights
sensorfile = "sensors.data"

subscribe = ["/actuator/lightint", "/actuator/flowpump", "/actuator/foodpump"]
