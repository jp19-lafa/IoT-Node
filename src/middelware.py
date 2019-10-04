import config

def middelware_waterlevel(level):
    """
    Tell us if the pump must be turned on or not
    Returns False if the pump must be turned off
    Returns True if the current state may stay the same
    """
    if(level > config.RISKY_WATER_LEVEL):
        return False
    # disable the pump when receiving faulty values
    if (level < 0):
        return False
    return True
