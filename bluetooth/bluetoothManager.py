import logger

def startup():
    logger.log("Starting up the bluetooth module", logger.LOG_DEBUG)

def idle():
    logger.log("Waiting for a bluetooth connection", logger.LOG_DEBUG)

def getWifiData():
    logger.log("Receiving wifi credentials", logger.LOG_DEBUG)

def EstablishConnection():
    startup()
    idle()
    getWifiData()
