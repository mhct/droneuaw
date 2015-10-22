__author__ = 'mario'

import Polygonal
from droneapi.lib import VehicleMode


class SafeBehaviour:
    """Defines a UAV behaviour."""

    def __init__(self, frequency = 1):
        pass

    def run(self):
        pass

class GeoFencingBehaviour(SafeBehaviour):
    """Defines a geo-fencing behaviour, not allowing the agent to fly outside it."""

    def __init__(self, fence, minimum_altitude, maximum_altitude, vehicle):
        SafeBehaviour.__init__(self,  20)
        self.fence = fence
        self.minimum_altitude = minimum_altitude
        self.maximum_altitude = maximum_altitude
        self.precision = 300 # Generates 300 probable locations for the UAV, using the GPS uncertainty
        self.vehicle = vehicle

    def run(self):
        """Executes the behaviour, creating a Command object with the desired actions to be taken by the UAV."""

        if self.vehicle.mode.name != "BRAKE" and self.vehicle.mode.name != "ALT_HOLD" and self.vehicle.mode.name != "LAND" and self.vehicle.mode.name != "RTL":
            gps_precision_in_decimal_degrees = Polygonal.centimetersToDecimalDegrees(self.vehicle.gps_0.eph)
            probable_drone_location = Polygonal.random_coordinates((self.vehicle.location.lat, self.vehicle.location.lon), gps_precision_in_decimal_degrees, self.precision)

            if Polygonal.points_in_poly(probable_drone_location, self.fence) is False:
                print "Broke circular fence."
                print self.vehicle.location
                print gps_precision_in_decimal_degrees

                return BrakeCommand()

            if self.vehicle.location.alt >= self.maximum_altitude  or self.vehicle.location.alt <= self.minimum_altitude:
                print "Broke altitude geo-fence."
                print self.vehicle.location
                print gps_precision_in_decimal_degrees

                return BrakeCommand()

        return NullCommand()


class BrakeCommand:
    def __call__(self):
        self.vehicle.mode = VehicleMode("BRAKE")
        self.vehicle.flush()


class NullCommand:
    def __call__(self):
        pass