
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
import bluetooth.config as config

LOG_ERROR = "[ERROR]" # type of logging
LOG_DEBUG = "[DEBUG]" # type of logging
LOG_WARM = "[WARN]" # type of logging

WARNING_COLOR = "\033[93m" # color for displaying warning messages
ERROR_COLOR = "\033[91m" # color for error messages
ENDC = "\033[0m" # end color sequence

def printInColor(type, text):
    """
    Display the right color based on the log type
    @Type is the log type as per defined in the above variables beginning with LOG_
    @text is the text to display
    """
    if (type == LOG_ERROR):
        print(ERROR_COLOR + type + " " + text + ENDC)
    elif (type == LOG_WARM):
        print(WARNING_COLOR + type + " " + text + ENDC)
    else:
        print(type, text)



def log(str, log_type=LOG_WARM):
    """
    Print a log based on its log_type
    """
    if(config.DEBUG):
        if(config.LOG_LEVEL == 3 and (log_type == LOG_WARM or log_type == LOG_DEBUG or log_type == LOG_ERROR)):
            printInColor(log_type, str)
        elif(config.LOG_LEVEL == 2 and log_type != LOG_DEBUG):
            printInColor(log_type, str )
        elif(log_type == LOG_ERROR):
            printInColor(log_type, str)

