import paho.mqtt.client as mqtt
import time
import config


class ID:
    """
    The ID class figures out if we already have an ID otherwise we get assigned one
    This should be used as a mqtt identifier. It is based around the current mac address
    """

    def __init__(self):
        from uuid import getnode as get_mac

        mac = get_mac()
        self.id = "".join(
            c + ":" if i % 2 else c for i, c in enumerate(hex(mac)[2:].zfill(12))
        )[:-1]

    def sensor(self):
        return self.id + ":aa"


class MQTT:
    """
        The mqtt class is the main class of this module.
        It handles the connection between the client and server.
        Important notes
        When you aren't sending information using MQTT.send()
        use MQTT.start() this will listen for incomming events
        And don't forget to call MQTT.end() before sending information
        When you don't need MQTT anymore use disconnect this will end the client connection
    """

    def __init__(self, host, port, password="", user="", useID=True):
        self.id = ID()
        if useID:
            self.client = mqtt.Client(client_id=self.id.id)
        else:
            self.client = mqtt.Client(client_id=self.id.sensor())
        self.client.username_pw_set(user, password)
        self.client.connect(host, port, 10)
        self.client.on_message = self.on_message

    def send(self, item, topic="node"):
        self.client.publish(topic, item)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def disconnect(self):
        print("Disconnected")
        self.client.disconnect()

    def start(self):
        self.client.loop_start()

    def end(self):
        self.client.loop_stop()

    # The callback for when a PUBLISH message is received from the server.
    # this should parse the information and propagate it
    # TODO: Handle received values here
    def on_message(self, client, userdata, msg):
        print("received topic: {}".format(msg.topic))


def eventHandler(server, topicList):
    """
    @Server is a mqtt connection
    @TopicList is an array of topics to subscribe to
    The eventHandler will subscribe to all topics in the list 
    And it will listen for MQTT connections
    """
    # TODO: send updated values from here
    while True:
        for topic in topicList:
            server.subscribe(server.id.id + topic)
        server.start()
        time.sleep(config.interval)
        server.send("15", ID().id + "/sensors/airhumidity")
        server.end()
    print("End of event loop")


if __name__ == "__main__":
    server = MQTT(config.server, config.port, user=config.user, password=config.passwd)
    print("Should be connected")

    eventHandler(server, config.subscribe)

    server.disconnect()
