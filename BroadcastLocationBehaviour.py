import json
import requests
__author__ = 'mario'

import SafeBehaviour

class BroadcastLocationBehaviour(SafeBehaviour.SafeBehaviour):
    """
    Defines a behaviour that broadcasts the location of the drone everytime it is executed.
    """

    def __init__(self, server_url, location):
        SafeBehaviour.SafeBehaviour.__init__(self,  20)
        self.server_url = server_url
        self.location = location
        self.i = 0

    def run(self):
        """Executes the behaviour, creating a Command object, asking the UAV to land
        FIXME remove this if from here and implement the scheduler
        """
        
        if self.i % 5 == 0:
            try:
                current_location = self.location.get_latest_location()
                ## sned the location in milimeters
                location_data = json.dumps({'type': 'Point', 'coordinates': [current_location[0]*1000, current_location[1]*1000, current_location[2]*1000]})
                requests.post(self.server_url, location_data)
            except:
                pass
            
        self.i = self.i + 1
        return SafeBehaviour.SafeBehaviour.do_nothing

