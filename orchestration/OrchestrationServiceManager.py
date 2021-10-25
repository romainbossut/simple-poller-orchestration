
from .OrchestrationService import OrchestrationService
"""

example input
my_service = [{"name": "mockservice", 
              "state_poller": MockPoller, 
              "interval": 1, 
              "state_dict": {}}, 
              {"name": "mockservice", 
              "state_poller": MockPoller, 
              "interval": 1, 
              "state_dict": {}}]




"""
class OrchestrationServiceManager:
    def __init__(self, services):
        self.services = services

    def run(self):
        for service in self.services:
            OrchestrationService(service["state_dict"], service["state_poller"], service["interval"]).run()

    def stop(self):
        for service in self.services:
            OrchestrationService(service["state_dict"], service["state_poller"], service["interval"]).stop()



