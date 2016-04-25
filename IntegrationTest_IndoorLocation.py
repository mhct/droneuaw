from dronekit import connect, Vehicle
from IndoorLocation import IndoorLocation
from time import sleep
from virtualenvironment.Server.Helper import Point

def setup():
    """Checks if vehicle is ready to execute script commands."""
#     print "Waiting for GPS..."
#     while vehicle.gps_0.fix_type < 1:
#         # gps_0.fix_type:
#         # 0-1: no fix
#         # 2: 2D fix, 3: 3D fix, 4: DGPS, 5: RTK
#         # check https://pixhawk.ethz.ch/mavlink/#GPS_RAW_INT
#         time.sleep(1)

#     print "Waiting for location..."
#     while vehicle.location.alt == 0.0:
#         time.sleep(1)

    while not vehicle.armed:
        print "Waiting for arming cycle completes..."
        sleep(1)


vehicle         = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)

# print "sleeping for 5 seconds to wait for vehicle connection"
# sleep(5)
# setup()

loc = IndoorLocation(vehicle)

i = 0
while True:
    point = loc.run()
    if i%5 == 0:
        print "Point: %.4f, %.4f, %.4f" %(point[0], point[1], point[2])
        print "Velocities: " + str(vehicle.velocity)
    i = i+1
    sleep(0.02)


