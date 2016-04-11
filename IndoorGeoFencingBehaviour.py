__author__ = 'mario'

import Polygonal
import SafeBehaviour
from dronekit.lib import VehicleMode


class IndoorGeoFencingBehaviour(SafeBehaviour.SafeBehaviour):
    """Defines a Indoors geo-fencing behaviour, not allowing the agent to fly in occupied areas"""

    def __init__(self, virtual_environment, minimum_altitude, maximum_altitude, vehicle):
        SafeBehaviour.SafeBehaviour.__init__(self,  20)
        self._virtual_environment = virtual_environment
        self.minimum_altitude = minimum_altitude
        self.maximum_altitude = maximum_altitude
        self.precision = 1 # Generates 1 probable locations for the UAV
        self.vehicle = vehicle
        self.adaptive_fence = False

    def set_adaptive_fence(self):
        self.adaptive_fence = True

    def run(self):
        """Executes the geo-fencing behaviour, returning a message either (halt, do_nothing)."""

        # TODO state machine for steering the drone away from forbiden zones
        # return SafeBehaviour.SafeBehaviour.halt

        # return SafeBehaviour.SafeBehaviour.do_nothing
        pass

# class BrakeCommand:
#     def __call__(self):
#         self.vehicle.mode = VehicleMode("BRAKE")
#         self.vehicle.flush()
#
#
# class NullCommand:
#     def __call__(self):
#         pass