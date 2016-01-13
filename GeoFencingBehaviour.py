__author__ = 'mario'

import Polygonal
import SafeBehaviour
from dronekit.lib import VehicleMode


class GeoFencingBehaviour(SafeBehaviour.SafeBehaviour):
    """Defines a geo-fencing behaviour, not allowing the agent to fly outside it."""

    def __init__(self, fence, minimum_altitude, maximum_altitude, vehicle):
        SafeBehaviour.SafeBehaviour.__init__(self,  20)
        self.fence = fence
        self.minimum_altitude = minimum_altitude
        self.maximum_altitude = maximum_altitude
        self.precision = 300 # Generates 300 probable locations for the UAV, using the GPS uncertainty
        self.vehicle = vehicle
        self.adaptive_fence = False

    def set_adaptive_fence(self):
        self.adaptive_fence = True

    def run(self):
        """Executes the geo-fencing behaviour, returning a message either (halt, do_nothing)."""

        if self.vehicle.mode.name != "BRAKE" and self.vehicle.mode.name != "ALT_HOLD" and self.vehicle.mode.name != "LAND" and self.vehicle.mode.name != "RTL":
            gps_precision_in_decimal_degrees = Polygonal.centimetersToDecimalDegrees(self.vehicle.gps_0.eph)
            probable_drone_locations = Polygonal.random_coordinates((self.vehicle.location.lat, self.vehicle.location.lon), gps_precision_in_decimal_degrees, self.precision)

            # Adaptive fence, predicts the location of the drone according to its velocity, after 1 second
            if self.adaptive_fence:
                def add_velocity(x): return (x[0] + self.vehicle.velocity[0], x[1] + self.vehicle.velocity[1])
                probable_drone_locations = map(add_velocity, probable_drone_locations)

            if Polygonal.points_in_poly(probable_drone_locations, self.fence) is False:
                print "Broke circular fence."
                print self.vehicle.location
                print gps_precision_in_decimal_degrees

                return SafeBehaviour.SafeBehaviour.halt

            if self.vehicle.location.alt >= self.maximum_altitude  or self.vehicle.location.alt <= self.minimum_altitude:
                print "Broke altitude geo-fence."
                print self.vehicle.location
                print gps_precision_in_decimal_degrees

                return SafeBehaviour.SafeBehaviour.halt

        return SafeBehaviour.SafeBehaviour.do_nothing


# class BrakeCommand:
#     def __call__(self):
#         self.vehicle.mode = VehicleMode("BRAKE")
#         self.vehicle.flush()
#
#
# class NullCommand:
#     def __call__(self):
#         pass