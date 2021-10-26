import logging

logger = logging.getLogger('root')


class Orchestrator:
    """
    This is a class that orchestrates the execution of tasks based on the state of the system.
    It uses a state poller to poll the state of the system and then uses a state dictionary to match the state of the system
    with the corresponding task to be executed.

    The state poller is an object of type StatePoller.
    The state dictionary is a dictionary of type {state: [task1, task2, ...]}
    Once a state is matched, all tasks associated to it are run in sequence

    The state poller is started by calling the start_poller() method of the state poller.
    The orchestrator is stopped by calling the stop() method.
    """


    def __init__(self, state_poller, state_dict):
        self.state_poller = state_poller
        self.state_dict = state_dict
        self.state = None
        self.previous_state = None
        self.state_task = None


    def poll_state(self):
        self.state = self.state_poller.poll_state()

        if self.state != self.previous_state:
            logger.info(" - state changed from {} to {}".format(self.previous_state, self.state))
        if self.state in self.state_dict:
            logger.info(" + state match found for {}".format(self.state))
            self.state_task = self.state_dict[self.state]
            for task in self.state_task:
                logger.info("     - Running task with function {}".format(task.get_function().__name__))
                task.run()
        else:
            logger.info("No matched task found for state {}".format(self.state))
        self.previous_state = self.state

    def get_previous_state(self):
        return self.previous_state

    def get_state(self):
        return self.state

    def stop(self):
        self.state_poller.stop_poller()