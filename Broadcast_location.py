import time
# import sys

import threading
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
import requests, json


drone_id = "a015c8dc-e033-4f16-b59f-d4a2dfc13977"
map_url = "http://127.0.0.1:9000/drones/" + drone_id + "/locations"

api             = local_connect()
vehicle         = api.get_vehicles()[0]

# lon = 4.678677
# lat = 50.863743
# alt = 20
# location_data = json.dumps({'type': 'Point', 'coordinates': [lon, lat, alt]})
# r = requests.post(map_url, location_data)

while not api.exit:
    location_data = json.dumps({'type': 'Point', 'coordinates': [vehicle.location.lon, vehicle.location.lat, vehicle.location.alt]})
    r = requests.post(map_url, location_data)
    time.sleep(0.3)


