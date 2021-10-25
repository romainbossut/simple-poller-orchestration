from .StatePoller import StatePoller
import random

class MockStatePoller(StatePoller):
    def __init__(self):
        super().__init__()
        self.state = "state1"

    def poll_state(self):
        self.state = random.choice(["state1", "state2", "state3", "state4", "state5"])
        return self.state
