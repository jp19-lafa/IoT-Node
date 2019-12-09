
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

import src.config as config
import src.motor as motor

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

def controlWaterPump(speed):
    """
    @speed is the speed of the water pump in percentage between 0 and 100
    """
    # TODO retreive the height of the water and toggle the motor based on the middleware value
    motor.receive(speed, config.pump)

def controlFood(speed):
    """
    @speed is the speed of the food pump in percentage between 0 and 100
    """
    # TODO: add middelware to protect from over saturation of food in water
    motor.receive(speed, config.food)

def controlLight(brightness):
    """
    @brightness is the brightness of the light in percentage between 0 and 100
    """
    # TODO: add light middelware check
    motor.receive(brightness, config.light)
