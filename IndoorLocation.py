__author__ = 'mario'

from virtualenvironment.Server.Helper import Point
from datetime import datetime

class IndoorLocation():
    """Keeps the location of the vehicle
    FIXME design. the problem with this design is that the location is updated in a reactive way,
    only when a client from the class asks for a new location. While actually, the location 
    should be updated when there is an interrupt or some kind of message which brings new information 
    about attitude changes.
    
    the complexity also increases since this object would need its own thread of execution, 
    and should be carefull with clients willing to get the location, or stale locations.s
    
    FIXME this class relies on having a precise velocity vector of the drone.
    TODO subscribe to attitude changes
    """

    def __init__(self, vehicle):
        if vehicle is None:
            raise "Vehicle can not be None."
        
        self.vehicle = vehicle
        self.reset_location()
    
    def reset_location(self):
        """ Resets the current location used in the vehicle."""
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.previous_time = datetime.now()
        
    
    def run(self):
        """Updates the location, given the average velocities of the vehicle
        
        :return location: current location [x,y,z] of the vehicle in meters (m) 
        :type Point:
        """
        current_time = datetime.now()
        time_delta = (current_time - self.previous_time).total_seconds()
        
        
        temp_velocity_vector = self.vehicle.velocity
        
        if temp_velocity_vector[0] >= 0.1:
            self.x = self.x + temp_velocity_vector[0] * time_delta
            
        if temp_velocity_vector[1] >= 0.1:
            self.y = self.y + temp_velocity_vector[1] * time_delta
            
#         self.z = self.z + temp_velocity_vector[2] * time_delta
        self.z = self.vehicle.location.global_frame.alt
        
        self.previous_time = current_time
        return Point(self.x, self.y, self.z)
    
    def get_latest_location(self):
        """Returns the latest location calculated by this class"""
        return (self.x, self.y, self.z)
    