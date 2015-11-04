__author__ = 'mario'
import sys
sys.path.insert(0, '/Users/mario/PycharmProjects/droneuaw')

import time
import GeoFencingBehaviour
import BatteryFailsafeBehaviour
import ForwardBehaviour
import SafeBehaviour

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
    while not vehicle.armed and not api.exit:
        time.sleep(1)


api             = local_connect()
vehicle         = api.get_vehicles()[0]

#
# Configures the geo-fence behaviour
#
fence = [(51.044277, 3.718161), (51.044331, 3.718165), (51.044317, 3.718271),(51.044260, 3.718260),(51.044277, 3.718161)]
fenceMax = 14
fenceMin = 4
geofence = GeoFencingBehaviour.GeoFencingBehaviour(fence, fenceMin, fenceMax)
battery_failsafe = BatteryFailsafeBehaviour.BatteryFailsafeBehaviour(api.get_battery())
forward = ForwardBehaviour.ForwardBehaviour()

level1 = {geofence: forward,
          battery_failsafe: forward,
          forward: None}

scheduler = SafeBehaviour.SafeScheduler(level1)

#
# Execution loop of the script
#
setup()
while not api.exit:
    time.sleep(0.05)
    # Not considering time, or scheduling
    scheduler.run()
