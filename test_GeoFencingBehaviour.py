__author__ = 'mario'

import SafeBehaviour
from GeoFencingBehaviour import GeoFencingBehaviour
import math


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

def test_AdaptiveFence():
    fence = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    minimum_altitude = 10
    maximum_altitude = 20
    vehicle = MockVehicle("LOITER", MockLocation(1,1,11))


    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, vehicle)
    b.set_adaptive_fence()

    vehicle.velocity = [0, 0, 0]
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing

    vehicle.velocity = [10, 10, 0]
    assert b.run() == SafeBehaviour.SafeBehaviour.halt

    vehicle.velocity = [9, 9, 0]
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing

    vehicle.velocity = [0, 9, 0]
    assert b.run() == SafeBehaviour.SafeBehaviour.do_nothing


def test_FenceWithGPSError():
    """
    Test using GPS error has to use floating numbers, otherwise the error is never big enough to show in the test.
    TODO improve this test to add randomness
    """
    fence = [(50.863862, 4.67886),(50.863613,  4.678992),(50.863613, 4.678625),(50.863789, 4.678523),(50.863862, 4.67886)]
    minimum_altitude = 10
    maximum_altitude = 20

    gps = MockGps()
    gps.eph = 900 # 9 meter horizontal GPS error

    vehicle = MockVehicle("LOITER", MockLocation(50.863743, 4.678677,11))
    vehicle.gps_0 = gps

    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, vehicle)
    b.precision = 700

    #
    # We want to receive a halt message with a certainty greater than 99%
    #
    certainty = 0.9
    accumulated_halts = 0
    runs = 1000
    for i in range(1,runs):
        if b.run() == SafeBehaviour.SafeBehaviour.halt:
            accumulated_halts = accumulated_halts + 1


    assert (accumulated_halts/float(runs)) >= certainty


def test_FenceWithGPSError():
    """
    Test using GPS error has to use floating numbers, otherwise the error is never big enough to show in the test.
    TODO improve this test to add randomness
    """
    fence = [(50.863862, 4.67886),(50.863613,  4.678992),(50.863613, 4.678625),(50.863789, 4.678523),(50.863862, 4.67886)]
    minimum_altitude = 10
    maximum_altitude = 20

    gps = MockGps()
    gps.eph = 900 # 9 meter horizontal GPS error

    vehicle = MockVehicle("LOITER", MockLocation(50.863743, 4.678677,11))
    vehicle.gps_0 = gps

    b = GeoFencingBehaviour(fence, minimum_altitude, maximum_altitude, vehicle)
    b.precision = 700

    #
    # We want to receive a halt message with a certainty greater than 99%
    #
    certainty = 0.9
    accumulated_halts = 0
    runs = 1000
    for i in range(1,runs):
        if b.run() == SafeBehaviour.SafeBehaviour.halt:
            accumulated_halts = accumulated_halts + 1


    assert (accumulated_halts/float(runs)) >= certainty
