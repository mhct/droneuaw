__author__ = 'mario'

import SafeBehaviour
from GeoFencingBehaviour import GeoFencingBehaviour

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
    def __init__(self, name = "RTL", location = MockLocation()):
        self.mode = MockMode(name)
        self.gps_0 = MockGps()
        self.location = location

def test_GeoFenceBehaviourNull():
    fence = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    minimum_altitude = 10
    maximum_altitude = 20

    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, MockVehicle("RTL"))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing

def test_GeoFenceBehaviourBrake():
    fence = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    minimum_altitude = 10
    maximum_altitude = 20
    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, MockVehicle("LOITER", MockLocation(1,1,1)))
    assert b.run() == SafeBehaviour.SafeBehaviour.halt

def test_GeoFenceBehaviourOK():
    fence = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    minimum_altitude = 10
    maximum_altitude = 20
    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, MockVehicle("LOITER", MockLocation(1,1,11)))
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing
