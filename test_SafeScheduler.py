__author__ = 'mario'

# fence = [(51.044277, 3.718161), (51.044331, 3.718165), (51.044317, 3.718271),(51.044260, 3.718260),(51.044277, 3.718161)]
# fenceMax = 14
# fenceMin = 4
# geofence = GeoFencingBehaviour.GeoFencingBehaviour(fence, fenceMin, fenceMax)
# battery_failsafe = BatteryFailsafeBehaviour.BatteryFailsafeBehaviour(api.get_battery())
# forward = ForwardBehaviour.ForwardBehaviour()
#
# level1 = {geofence: forward,
#           battery_failsafe: forward,
#           forward: None}
#
# scheduler = SafeBehaviour.SafeScheduler(level1)

import SafeBehaviour
import ForwardBehaviour

# def test_scheduler():
#     level1 = {None: None}
#
#     scheduler = SafeBehaviour.SafeScheduler(level1)
#     scheduler.run()

class FakeBehaviour:
    def run(self):
        return SafeBehaviour.SafeBehaviour.halt

def test_scheduler1():
    level1 = {ForwardBehaviour.ForwardBehaviour(): []}

    scheduler = SafeBehaviour.SafeScheduler(level1)
    scheduler.run()

def test_scheduler_brake():
    forward = ForwardBehaviour.ForwardBehaviour()
    fake = FakeBehaviour()

    level1 = {fake: [forward],
              forward: []}

    scheduler = SafeBehaviour.SafeScheduler(level1)
    scheduler.run()