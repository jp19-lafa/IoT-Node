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
import pigpio
import src.config as config
from time import sleep
pi = pigpio.pi()



def controlWaterPump(speed):
    """
    @speed is the speed of the water pump in percentage between 0 and 100
    """
    # TODO retreive the height of the water and toggle the motor based on the middleware value
    receive(speed, config.pump)

def controlFood(speed):
    """
    @speed is the speed of the food pump in percentage between 0 and 100
    """
    # TODO: add middelware to protect from over saturation of food in water
    receive(speed, config.food)

def controlLight(brightness):
    """
    @brightness is the brightness of the light in percentage between 0 and 100
    """
    # TODO: add light middelware check
    receive(brightness, config.light)

# Convert received value to a dutycyle on the received pin
def receive(payload, pin):
    """
    Convert the received data to a pwm signal on the pin
    """
    val = payload
    if type(payload) is str:
        val = int(float("".join(payload)))
    print("Value in percent {}".format(val))
    val = int(val*2.55)
    print("Calculated value {}".format(val))
    val = val if val < 255 else 255
    val = val if val > 0 else 0
    pi.set_PWM_dutycycle(pin, val)

class stepper:
    def __init__(self, dirPin, stepPin, sleepPin, Resolution=1):
        """
        @Dirpin is the pin to change the direction of the motor
        @Steppin is the pin to toggle in order for the stepper motor to rotate once
        @SleepPin is the pin to turn of the motor driver
        @Resolution is the precision of the driver (microstepping)
        """
        self.dirPin = dirPin
        self.stepPin = stepPin
        self.sleepPin = sleepPin
        self.Resolution = Resolution
        self.SPR = (360/1.8) * Resolution

    def turn_degrees(self, degrees, dir, delay=1):
        """
        Rotate to motor at a given speed
        @degrees is the amount of degrees to rotate the motor shaft
        @dir is in which direction to turn (0 or 1)
        @delay is the speed of rotation for a full turn
        """
        pi.write(self.dirPin, dir)
        pi.write(self.sleepPin, 1)
        sleep(0.5)
        delay = delay / self.SPR # time to take per step
        for x in range(int((degrees/360) * SPR)):
            pi.write(self.stepPin, 1)
            sleep(delay)
            pi.write(self.stepPin, 0)
            sleep(delay)
        pi.write(self.sleepPin,0)