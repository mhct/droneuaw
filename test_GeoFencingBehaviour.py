__author__ = 'mario'

from GeoFencingBehaviour import GeoFencingBehaviour, BrakeCommand, NullCommand

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
    assert isinstance(b.run(), NullCommand)

def test_GeoFenceBehaviourBrake():
    fence = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    minimum_altitude = 10
    maximum_altitude = 20
    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, MockVehicle("LOITER", MockLocation(1,1,1)))
    assert isinstance(b.run(), BrakeCommand)

def test_GeoFenceBehaviourOK():
    fence = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    minimum_altitude = 10
    maximum_altitude = 20
    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, MockVehicle("LOITER", MockLocation(1,1,11)))
    assert isinstance(b.run(), NullCommand)
