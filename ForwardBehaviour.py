__author__ = 'mario'

import Polygonal
from dronekit.lib import VehicleMode
import SafeBehaviour



class ForwardBehaviour(SafeBehaviour.SafeBehaviour):
    """
    Defines a battery failsafe behaviour.

    This behaviour detects if the batter is below a certain threshold and starts landing.
    """

    def __init__(self, vehicle):
        SafeBehaviour.SafeBehaviour.__init__(self, 20)
        self.vehicle = vehicle
        self.commands = []

    def run(self):
        """Executes the behaviour, creating a Command object, asking the UAV to land."""

        #TODO improve this.. add FSM taking care of current state (landing, breaking, etc) check rules
        # for iterating over the commands list

        for i in range(0, len(self.commands)):
            c = self.commands.pop()

            if c == SafeBehaviour.SafeBehaviour.land:
                self.commands = []
                return LandCommand(self.vehicle)

            if c == SafeBehaviour.SafeBehaviour.halt:
                return BrakeCommand(self.vehicle)

        return SafeBehaviour.SafeBehaviour.none

    def addCommand(self, command):
        self.commands.append(command)


class BrakeCommand:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def __call__(self):
        self.vehicle.mode = VehicleMode("BRAKE")
        self.vehicle.flush()

class LandCommand:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def __call__(self):
        self.vehicle.mode = VehicleMode("LAND")
        self.vehicle.flush()
