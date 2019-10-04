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