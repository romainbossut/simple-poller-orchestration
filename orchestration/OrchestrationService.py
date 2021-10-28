from .Orchestrator import Orchestrator
from .Scheduler import Scheduler
import logging

logger = logging.getLogger('root')


# an OrchestrationService that take a state / task dictionary as input, the poller,  an interval, set ups an a orchestrator and scheduler and runs it
class OrchestrationService:
    def __init__(self, name, state_dict, state_poller, interval):
        self.state_dict = state_dict
        self.state_poller = state_poller
        self.interval = interval
        self.scheduler = None
        self.name = name

    def run(self):
        orchestrator = Orchestrator(self.state_poller, self.state_dict)
        self.scheduler = Scheduler(orchestrator, self.interval)
        self.scheduler.run()
        print("---- Service {} scheduler started".format(self.name))

    def stop(self):
        self.scheduler.terminate()
        print("---- Service {} scheduler stopped".format(self.name))

