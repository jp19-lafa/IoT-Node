
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

import unittest
import middelware
import config

class TestMiddelWareMethods(unittest.TestCase):
    def test_sensorHandlerWaterLevelHigh(self):
        """
        Test if the current water level is to high. If so the middelware should disable the node.
        """
        waterlevel = 255
        bIsAllowedToRun = middelware.middelware_waterlevel(waterlevel)
        self.assertTrue(not bIsAllowedToRun)

    def test_sensorHandlerWaterLevelLow(self):
        """
        Test if the current water level is to high. If so the middelware should disable the node
        """
        waterlevel = 100
        bIsAllowedToRun = middelware.middelware_waterlevel(waterlevel)
        self.assertTrue(bIsAllowedToRun)

    def test_sensorHandlerWaterLevelLimit(self):
        """
        Test if the current water level is to high. If so the middelware should disable the node
        """
        waterlevel = config.RISKY_WATER_LEVEL
        bIsAllowedToRun = middelware.middelware_waterlevel(waterlevel)
        self.assertTrue(bIsAllowedToRun)

    def test_sensorHandlerWaterLevelUnderZero(self):
        """
        Test if the current water level is to high. If so the middelware should disable the node
        """
        waterlevel = -5
        bIsAllowedToRun = middelware.middelware_waterlevel(waterlevel)
        self.assertTrue(not bIsAllowedToRun)

    def test_sensorHandlerWaterLevelAbove255(self):
        """
        Test if the current water level is to high. If so the middelware should disable the node
        """
        waterlevel = 300
        bIsAllowedToRun = middelware.middelware_waterlevel(waterlevel)
        self.assertTrue(not bIsAllowedToRun)


if __name__ == '__main__':
    unittest.main()
