__author__ = 'mario'

import SafeBehaviour.SafeBehaviour as SafeBehaviour

class BatteryFailsafeBehaviour(SafeBehaviour):
    """
    Defines a battery failsafe behaviour.

    This behaviour detects if the batter is below a certain threshold and starts landing.
    """

    def __init__(self, battery, minimum_voltage):
        SafeBehaviour.__init__(self,  20)
        self.battery = battery
        self.minimum_voltage = minimum_voltage


    def run(self, inbox = None):
        """Executes the behaviour, creating a Command object, asking the UAV to land"""

        #TODO this is wrong, the state should be local...
        if self.vehicle.mode.name != "LAND":
            if self.battery.voltage <= self.minimum_voltage:
                return SafeBehaviour.land

        return SafeBehaviour.SafeBehaviour.do_nothing

