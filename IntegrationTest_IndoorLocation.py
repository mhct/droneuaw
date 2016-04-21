from dronekit import connect, Vehicle
from IndoorLocation import IndoorLocation
from time import sleep
from virtualenvironment.Server.Helper import Point

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


vehicle         = connect('/dev/ttyACM0', wait_ready=True)
setup()

loc = IndoorLocation(vehicle)

i = 0
while True:
    point = loc.run()
    if i%100 == 0:
        print "Point: %.2d, %.2d, %.2d" %(point[0], point[1], point[2])
    i = i+1
    sleep(0.02)


