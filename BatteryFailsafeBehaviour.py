__author__ = 'mario'

import SafeBehaviour

class BatteryFailsafeBehaviour(SafeBehaviour.SafeBehaviour):
    """
    Defines a battery failsafe behaviour.

    If the battery is below a certain threshold, the behaviour sends a message requesting to land.
    """

    def __init__(self, battery, minimum_voltage, vehicle):
        SafeBehaviour.SafeBehaviour.__init__(self,  20)
        self.battery = battery
        self.minimum_voltage = minimum_voltage
        self.vehicle = vehicle


    def run(self):
        """Executes the behaviour, creating a Command object, asking the UAV to land"""

        #TODO this is wrong, the state should be local...or not
        if self.vehicle.mode.name != "LAND":
            if abs(self.battery.voltage - self.minimum_voltage) <= 0.01:
                return SafeBehaviour.land

        return SafeBehaviour.SafeBehaviour.do_nothing

