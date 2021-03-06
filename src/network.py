
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

import src.config as config
import paho.mqtt.client as mqtt
import src.sensordata as sensordata
import src.motor as motor
import src.logger as logger

class ID:
    """
    The ID class figures out if we already have an ID otherwise we get assigned one
    This should be used as a mqtt identifier. It is based around the current mac address
    """

    def __init__(self):
        from uuid import getnode as get_mac

        mac = get_mac()
        self.id = "".join(c + ":" if i % 2 else c
                          for i, c in enumerate(hex(mac)[2:].zfill(12)))[:-1]

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
        self.id = config.mac
        if useID:
            self.client = mqtt.Client(client_id=self.id)
        else:
            self.client = mqtt.Client(client_id=self.id)
        self.client.username_pw_set(user, password)
        self.client.connect(host, port, 10)
        self.client.on_message = self.on_message

    def send(self, item, topic="node"):
        self.client.publish(topic, item)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def disconnect(self):
        logger.log("MQTT server disconnected", logger.LOG_ERROR)
        self.client.disconnect()

    def start(self):
        self.client.loop_start()

    def end(self):
        self.client.loop_stop()

    # The callback for when a PUBLISH message is received from the server.
    # this should parse the information and propagate it
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = float(msg.payload.decode("utf-8")) 
        prefix = config.MQTT_ENDPOINT_PREFIX + self.id
        logger.log("Payload in percent {}".format(payload), logger.LOG_DEBUG)
        if topic == prefix + config.subscribe[0]:
            # TODO: call motor values
            logger.log("send to light", logger.LOG_DEBUG) 
            motor.controlLight(payload)
        elif topic == prefix + config.subscribe[1]:
            # TODO: call motor values
            logger.log("send to flowpump", logger.LOG_DEBUG) 
            motor.controlFood(payload)
        elif topic == prefix + config.subscribe[2]:
            # TODO: call motor values
            logger.log("sending to foodpump", logger.LOG_DEBUG)
            motor.controlWaterPump(payload)

        else:
            logger.log("Unknown topic", logger.LOG_ERROR)


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
        # start time listner
        t0 = time.time()
        # receive actuator data
        for topic in topicList:
            server.subscribe(config.MQTT_ENDPOINT_PREFIX + server.id + topic)
            logger.log("Subscribe event: " + config.MQTT_ENDPOINT_PREFIX + server.id + topic, logger.LOG_DEBUG)
        # send sensor data
        for data in sensordata.readAll():
            server.send(data.payload, config.MQTT_ENDPOINT_PREFIX + server.id + data.topic)
            logger.log("Uploading to {} with data {}".format(config.MQTT_ENDPOINT_PREFIX + server.id + data.topic, data.payload))
        t1 = time.time()
        time.sleep(config.interval)
        logger.log("Event loop finished {} seconds and slept for {} seconds".format(t1-t0, config.interval), logger.LOG_DEBUG)
        server.end()
    logger.log("EventHandler has stopped", logger.LOG_ERROR)


if __name__ == "__main__":
    server = MQTT(config.server,
                  config.port,
                  user=config.user,
                  password=config.passwd)
    logger.log("Connected with MQTT server", logger.LOG_DEBUG)

    eventHandler(server, config.subscribe)

    server.disconnect()
