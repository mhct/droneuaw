from virtualenvironment.Server.VirtualEnvironment import VirtualEnvironment
from virtualenvironment.Server.Helper import CellSize, MapParams, MapWidth
__author__ = 'mario'

import SafeBehaviour
from IndoorGeoFencingBehaviour import IndoorGeoFencingBehaviour


class MockMode:
    def __init__(self, name):
        self.name = name

class MockGps:
    def __init__(self):
        self.eph = 0

class MockLocation:
    def __init__(self, lat=0, lon=0, alt=0):
        self.lat = lat
        self.lon = lon
        self.alt = alt

class MockVehicle:
    def __init__(self, name = "RTL", location = MockLocation(), velocity = (0,0,0)):
        self.mode = MockMode(name)
        self.gps_0 = MockGps()
        self.location = location
        self.velocity = velocity


def test_GeoFenceBehaviourNull():
    b = IndoorGeoFencingBehaviour("", 0, 10, MockVehicle("RTL"))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt
    
def test_small_altitudes():
    virtual_env = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 5000, MockVehicle("RTL", MockLocation(0, 0, 0.00002)))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing

    b = IndoorGeoFencingBehaviour(virtual_env, 0, 5000, MockVehicle("RTL", MockLocation(0, 0, 0.00001)))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt
    
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 5000, MockVehicle("RTL", MockLocation(0, 0, 1)))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing

    

def test_large_altitudes():
    virtual_env = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", MockLocation(0, 0, 9.98)))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing
    
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", MockLocation(0, 0, 10)))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt
    
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", MockLocation(0, 0, 6)))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing
    
  
def test_inside_virtual_environment():
    virtual_env = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))
 
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", MockLocation(4, 4, 5)))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing
      

def test_outside_virtual_environment():
    virtual_env = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))
    
    drone_location = MockLocation(0, 0, 10);
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", drone_location))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt
    
    drone_location = MockLocation(5.1, 0, 5);
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", drone_location))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt
    
    drone_location = MockLocation(0, 5.1, 5);
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", drone_location))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt

    drone_location = MockLocation(10, 10, -5);
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", drone_location))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt
    
def test_adaptive_fence_standing_still():
    virtual_env = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))

    drone_location = MockLocation(5, 5, 5);
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", drone_location))
    b.set_adaptive_fence()
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing
    
def test_adaptive_fence_standing_still_near_boundary():
    virtual_env = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))

    drone_location = MockLocation(0, 0, 5);
    b = IndoorGeoFencingBehaviour(virtual_env, 0, 10000, MockVehicle("RTL", drone_location), 1, 1000)
    b.set_adaptive_fence()
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing
    