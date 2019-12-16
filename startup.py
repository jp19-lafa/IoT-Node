import src.network as network
import src.config as config
import pair.main as blue

if __name__ == "__main__":
    blue.startup()
    server = network.MQTT(config.server,
                  config.port,
                  user=config.user,
                  password=config.passwd)
    print("Should be connected")

    network.eventHandler(server, config.subscribe)

    server.disconnect()
