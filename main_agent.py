__author__ = 'mario'
from dronekit import connect

import sys
# sys.path.insert(0, '/Users/mario/PycharmProjects/droneuaw/droneuaw')

import time
import GeoFencingBehaviour
import IndoorGeoFencingBehaviour
import BatteryFailsafeBehaviour
import ForwardBehaviour
import SafeBehaviour
from  virtualenvironment.Server import HttpServer

# import threading

def setup():
    """Checks if vehicle is ready to execute script commands."""
    print "Waiting for GPS..."
    while vehicle.gps_0.fix_type < 2:
        # gps_0.fix_type:
        # 0-1: no fix
        # 2: 2D fix, 3: 3D fix, 4: DGPS, 5: RTK
        # check https://pixhawk.ethz.ch/mavlink/#GPS_RAW_INT
        time.sleep(1)

    print "Waiting for location..."
    while vehicle.location.alt == 0.0:
        time.sleep(1)

    print "Waiting for arming cycle completes..."
    #while not vehicle.armed:
    #    time.sleep(1)


vehicle         = connect('127.0.0.1:14550', wait_ready=True)

#
# Configures the geo-fence behaviour
#
# fence = [(51.044277, 3.718161), (51.044331, 3.718165), (51.044317, 3.718271),(51.044260, 3.718260),(51.044277, 3.718161)]
# fenceMax = 14
# fenceMin = 4
# geofence = GeoFencingBehaviour.GeoFencingBehaviour(fence, fenceMin, fenceMax, vehicle)

app = HttpServer.app
app.config['TESTING'] = False
server_name = "127.0.0.1:7000"
URL = "http://" + server_name
app.config['SERVER_NAME'] = server_name

geofence = IndoorGeoFencingBehaviour.IndoorGeoFencingBehaviour(HttpServer._virtual_environment, minimum_altitude=0.0, maximum_altitude=4000, vehicle)

forward = ForwardBehaviour.ForwardBehaviour(vehicle)

#import pdb; pdb.set_trace()

level1_behaviours = {geofence: [forward]}


if hasattr(vehicle, "battery") == True:
    battery_failsafe = BatteryFailsafeBehaviour.BatteryFailsafeBehaviour(vehicle.battery, 10.5, vehicle)
    level1_behaviours[battery_failsafe] = [forward]


level1_behaviours[forward] = []

# level1_behaviours = {geofence: [forward],
#           battery_failsafe: [forward],
#           forward: []}

scheduler = SafeBehaviour.SafeScheduler(level1_behaviours)

#
# Execution loop of the script
#
setup()
while True:
    time.sleep(0.05)
    # Not considering time, or scheduling
    scheduler.run()
