
# create an abstract class StatePoller that polls the state of the API and returns it
class StatePoller:
    def __init__(self):
        self.state = None

    def poll_state(self):
        return self.state