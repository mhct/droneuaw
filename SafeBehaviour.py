__author__ = 'mario'


class SafeBehaviour:
    """Defines a UAV behaviour."""

    halt = "Halt"
    do_nothing = "DoNothing"
    none = ""
    land = "Land"

    def __init__(self, frequency = 1):
        pass

    def run(self):
        pass

    def addCommand(self):
        pass


class SafeScheduler:

    def __init__(self, behaviours_graph = {}):
        self.behaviours_graph = behaviours_graph
        print "Initializing Scheduler"

    def run(self):
        """Executes each behaviour, handles behaviour communication and command execution."""
        for behaviour in self.behaviours_graph.keys():
            command = behaviour.run()

            if isinstance(command, str):
                # propagates command to all associated components
                for target in self.behaviours_graph[behaviour]:
                    target.addCommand(command)
            else:
                command()
