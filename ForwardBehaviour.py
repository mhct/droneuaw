__author__ = 'mario'

import Polygonal
from droneapi.lib import VehicleMode
import SafeBehaviour



class ForwardBehaviour(SafeBehaviour.SafeBehaviour):
    """
    Defines a battery failsafe behaviour.

    This behaviour detects if the batter is below a certain threshold and starts landing.
    """

    def __init__(self):
        SafeBehaviour.SafeBehaviour.__init__(self,  20)
        self.commands = []

    def run(self):
        """Executes the behaviour, creating a Command object, asking the UAV to land"""

        ret = None

        for i in range(0, len(self.commands)):
            c = self.commands.pop()

            if c == SafeBehaviour.SafeBehaviour.land:
                self.commands = []
                return LandCommand()

            if c == SafeBehaviour.SafeBehaviour.halt:
                return BrakeCommand()

        return SafeBehaviour.SafeBehaviour.none

    def addCommand(self, command):
        self.commands.append(command)


class BrakeCommand:
    def __call__(self):
        self.vehicle.mode = VehicleMode("BRAKE")
        self.vehicle.flush()

class LandCommand:
    def __call__(self):
        self.vehicle.mode = VehicleMode("LAND")
        self.vehicle.flush()
