__author__ = 'mario'

from BroadcastLocationBehaviour import BroadcastLocationBehaviour
from IndoorLocation import IndoorLocation
import thread
from dronekit import connect
import time
import IndoorGeoFencingBehaviour
import BatteryFailsafeBehaviour
import ForwardBehaviour
import SafeBehaviour
from  virtualenvironment.Server import HttpServer

# import sys
# sys.path.insert(0, '/Users/mario/PycharmProjects/droneuaw/droneuaw')
# import threading

def setup(useGPS=False, waitArming=False):
    """Checks if vehicle is ready to execute script commands."""
    
    if useGPS:
        while vehicle.gps_0.fix_type < 2:
            print "Waiting for GPS..."
            # gps_0.fix_type:
            # 0-1: no fix
            # 2: 2D fix, 3: 3D fix, 4: DGPS, 5: RTK
            # check https://pixhawk.ethz.ch/mavlink/#GPS_RAW_INT
            time.sleep(1)

    while vehicle.location.alt == 0.0:
        print "Waiting for location..."
        time.sleep(1)

    if waitArming:
        while not vehicle.armed:
            print "Waiting for arming cycle completes..."
            time.sleep(1)


# vehicle         = connect('127.0.0.1:14550', wait_ready=True)
#vehicle         = connect('/dev/tty.usbmodem1', wait_ready=True)
vehicle         = connect('/dev/ttyAMA0', baud=57600, wait_ready=True)

#
# Configures the geo-fence behaviour
#
# fence = [(51.044277, 3.718161), (51.044331, 3.718165), (51.044317, 3.718271),(51.044260, 3.718260),(51.044277, 3.718161)]
# fenceMax = 14
# fenceMin = 4
# geofence = GeoFencingBehaviour.GeoFencingBehaviour(fence, fenceMin, fenceMax, vehicle)

map_server_url = "http://192.168.1.3:5000/drones/1/locations" #FIXME add as configuration option
#
# Configures and starts HTTP SERVER
#
app = HttpServer.app
app.config['TESTING'] = False
server_name = "localhost:7000"
URL = "http://" + server_name
app.config['SERVER_NAME'] = server_name
def flaskThread():
    app.run()
    
thread.start_new_thread(flaskThread,())
#
# end configuration HTTPServer
#


location = IndoorLocation(vehicle)

#
# behaviours
#
geofence = IndoorGeoFencingBehaviour.IndoorGeoFencingBehaviour(HttpServer._virtual_environment, minimum_altitude=0.0, maximum_altitude=4000, vehicle=vehicle, location=location)
location_broadcast = BroadcastLocationBehaviour(map_server_url, location)
forward = ForwardBehaviour.ForwardBehaviour(vehicle)

#import pdb; pdb.set_trace()

level1_behaviours = {geofence: [forward]}
level1_behaviours[location_broadcast] = [forward]

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
i=0
while True:
    time.sleep(0.05)
    if HttpServer.get_reset_pose():
        print "reset location received"
        location.reset_location()
        HttpServer.set_reset_pose_false()
        print location.get_latest_location()
        
    # Not considering time, or scheduling
    scheduler.run()
    
    if i%100 == 0:
        print location.get_latest_location()
    i = i + 1
        

