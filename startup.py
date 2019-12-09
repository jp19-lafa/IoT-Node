import src.network as network
import src.config as config

if __name__ == "__main__":
    server = network.MQTT(config.server,
                  config.port,
                  user=config.user,
                  password=config.passwd)
    print("Should be connected")

    network.eventHandler(server, config.subscribe)

    server.disconnect()
