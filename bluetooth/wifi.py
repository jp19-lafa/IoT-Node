import urllib
import config

def ConnectedToTheNetwork():
    try:
        urllib.urlopen(config.NETWORK_CHECK, timeout=config.NETWORK_TIMEOUT)
        return True
    except: 
        return False