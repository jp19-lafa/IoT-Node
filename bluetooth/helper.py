import config

LOG_ERROR = "[ERROR]"
LOG_DEBUG = "[DEBUG]"
LOG_WARM = "[WARN]"

WARNING_COLOR = "\033[93m" # color for displaying warning messages
ERROR_COLOR = "\033[91m" # color for error messages
ENDC = "\033[0m" # end color sequence

def printInColor(type, text):
    if (type == LOG_ERROR):
        print(ERROR_COLOR + type + " " + text + ENDC)
    elif (type == LOG_WARM):
        print(WARNING_COLOR + type + " " + text + ENDC)
    else:
        print(type, text)



def log(str, log_type=LOG_WARM):
    """
    Print a log
    """
    if(config.DEBUG):
        if(config.LOG_LEVEL == 3 and (log_type == LOG_WARM or log_type == LOG_DEBUG or log_type == LOG_ERROR)):
            printInColor(log_type, str)
        elif(config.LOG_LEVEL == 2 and log_type != LOG_DEBUG):
            printInColor(log_type, str )
        elif(log_type == LOG_ERROR):
            printInColor(log_type, str)

