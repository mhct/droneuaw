import Polygonal
__author__ = 'mario'

import SafeBehaviour
from virtualenvironment.Server.Helper import Point

class IndoorGeoFencingBehaviour(SafeBehaviour.SafeBehaviour):
    """Defines a Indoors geo-fencing behaviour, not allowing the agent to fly in occupied areas"""

    def __init__(self, virtual_environment, minimum_altitude, maximum_altitude, vehicle, error_margin = 0.1, precision = 1):
        """
        Creates the behaviour for flying inside a indoors geo-fence
        
        :param virtual_environment: the object representing the virtual environment
        :type virtual_environment: VirtualEnvironment
        
        :param minimum_altitude: the minimum altitude the drone is allowed to fly inside the geo-fence in Milimeters
        :type minimum_altitude: float
        
        :param maximum_altitude: the maximum altitude the drone is allowed to fly inside the geo-fence in Milimeters 
        :type maximum_altitude: float
        
        :param vehicle: the object representing the vehicle, containing attitude information
        :type vehicle: Vehicle

        :param error_margin: expected error in the sensors (measured in meters)
        :type error_margin: float
        
        :param precision: number of coordinates to be generated to estimate the REAL location of the vehicle
        :type precision: int
        """
        if virtual_environment is None:
            raise "VirtualEnvironment can not be None."
        
        SafeBehaviour.SafeBehaviour.__init__(self,  20)
        self._virtual_environment = virtual_environment
        self.minimum_altitude = minimum_altitude
        self.maximum_altitude = maximum_altitude
        self.error_margin = error_margin #FIXME add to constructor parameter
        self.precision = precision # FIXME add to contructor parameter. Generates 1 probable locations for the UAV
        self.vehicle = vehicle
        self.adaptive_fence = False

    def set_adaptive_fence(self):
        self.adaptive_fence = True

    def run(self):
        """Executes the geo-fencing behaviour, returning a message either (halt, do_nothing)."""

        # TODO state machine for steering the drone away from forbiden zones
        # return SafeBehaviour.SafeBehaviour.halt
        command = SafeBehaviour.SafeBehaviour.none
        
        probable_drone_locations = []
                
        # location of vehicle in milimeters MM
        vehicle_location = Point(self.vehicle.location.lat*1000, self.vehicle.location.lon*1000, self.vehicle.location.alt*1000)
        

        # Adaptive fence, predicts the location of the drone according to its velocity, after 1 second
        if self.adaptive_fence:
            probable_drone_locations = Polygonal.random_coordinates_3d(vehicle_location, 
                                                                   self.error_margin,
                                                                   self.precision)
            
            def add_velocity(x): return Point(x[0] + self.vehicle.velocity[0]*1000, x[1] + self.vehicle.velocity[1]*1000, x[2] + self.vehicle.velocity[2]*1000)
     
            probable_drone_locations = map(add_velocity, probable_drone_locations)
        else:
            probable_drone_locations = [vehicle_location]

        for point in probable_drone_locations:
            if (point[2] - self.maximum_altitude) < -0.01 and (point[2] - self.minimum_altitude) > 0.01:
                try:
                    if self._virtual_environment.is_occupied(point) is True:
                        command = SafeBehaviour.SafeBehaviour.halt
                        break
                    else:   
                        command = SafeBehaviour.SafeBehaviour.do_nothing
                except:
                    command = SafeBehaviour.SafeBehaviour.halt
                    break
            else:
                command = SafeBehaviour.SafeBehaviour.halt
                break
                

        return command