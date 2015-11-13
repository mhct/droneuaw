__author__ = 'mario'


import SafeBehaviour
import ForwardBehaviour

# def test_scheduler():
#     level1 = {None: None}
#
#     scheduler = SafeBehaviour.SafeScheduler(level1)
#     scheduler.run()

class FakeBehaviour:
    def __init__(self):
        self.executed = 0

    def run(self):
        self.executed += 1
        return SafeBehaviour.SafeBehaviour.halt

class FakeForwardBehaviour:

    def __init__(self):
        self.run_executed = 0
        self.commands = []

    def run(self):
        self.run_executed +=1
        return lambda : ()

    def addCommand(self, command):
        self.commands.append(command)


def test_scheduler1():
    level1 = {ForwardBehaviour.ForwardBehaviour(): []}

    scheduler = SafeBehaviour.SafeScheduler(level1)
    scheduler.run()

def test_scheduler_brake():
    """Tests two behaviours, one FakeBehaviour, which sends a 'halt' message, and the ForwardBehaviour."""

    forward = FakeForwardBehaviour()
    fake = FakeBehaviour()

    level1 = {fake: [forward],
              forward: []}

    scheduler = SafeBehaviour.SafeScheduler(level1)
    scheduler.run()

    assert 1 == fake.executed
    assert 1 == forward.run_executed
    assert [SafeBehaviour.SafeBehaviour.halt] == forward.commands

def test_scheduler_1_to_2behaviours():
    """Tests if the scheduler sends messages to all target behaviours."""

    forward = FakeForwardBehaviour()
    fake = FakeBehaviour()
    do_nothing = FakeForwardBehaviour()

    level1 = {fake: [forward, do_nothing],
              forward: [],
              do_nothing: []}

    scheduler = SafeBehaviour.SafeScheduler(level1)
    scheduler.run()

    assert [SafeBehaviour.SafeBehaviour.halt] == forward.commands
    assert [SafeBehaviour.SafeBehaviour.halt] == do_nothing.commands

def test_scheduler_2_to_1behaviours():
    """Tests if the scheduler sends messages from all soources to target behaviours."""

    forward = FakeForwardBehaviour()
    fake = FakeBehaviour()
    do_nothing = FakeBehaviour()

    level1 = {fake: [forward],
              do_nothing: [forward],
              forward: []}

    scheduler = SafeBehaviour.SafeScheduler(level1)
    scheduler.run()

    assert [SafeBehaviour.SafeBehaviour.halt, SafeBehaviour.SafeBehaviour.halt] == forward.commands
