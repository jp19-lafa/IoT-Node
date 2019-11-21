import socket
import config
import logger

def ConnectedToTheNetwork():
     try:
        socket.setdefaulttimeout(config.NETWORK_TIMEOUT)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((config.NETWORK_CHECK, config.NETWORK_PORT))
        return True
     except socket.error as ex:
        logger.log("No connection is present to the internet. {}".format(ex), logger.LOG_ERROR)
        return False # this should change once deployed