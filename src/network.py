
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

import time

import config
import sensordata
import paho.mqtt.client as mqtt


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
        server.start()
        for topic in topicList:
            server.subscribe(server.id.id + topic)
            print(server.id.id + topic)
        time.sleep(config.interval)
        for data in sensordata.readAll():
            server.send(data.payload, ID().id + data.topic)
        server.end()
    print("End of event loop")


if __name__ == "__main__":
    server = MQTT(config.server, config.port, user=config.user, password=config.passwd)
    print("Should be connected")

    eventHandler(server, config.subscribe)

    server.disconnect()
