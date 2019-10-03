class Payload():
    """
    Payload to send data over a mqtt connection
    """
    def __init__(self, payload, topic):
        self.payload = payload
        self.topic = topic

def readAll():
    """
    Read all sensors out. Build a MQTT payload and send it over
    """
    return [Payload("15", "/sensors/airhumidity"), Payload("hello", "/sensors/random")]