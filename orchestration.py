# create a class orchestrator, that polls a state from an api, has a dictionary of possible states linked to a Task and run them
import threading
import datetime
import time
import random


# set up a logger and loggin capability
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a handler and set level to info
handler = logging.FileHandler("orchestration.log")
logger.addHandler(logging.StreamHandler())
handler.setLevel(logging.INFO)


# create a class that can be called to run a function
class Task:
    """
    This is a class that defines a task to be run.

    Args:
        function (function): The function to be run.
        *args (list): The arguments to be passed to the function.
        max_retry (int): The maximum number of times to retry running the function
            in case of an exception.

    Attributes:
        function (function): The function to be run.
        args (list): The arguments to be passed to the function.
        retry_count (int): The number of times the function has been retried.
        max_retry (int): The maximum number of times to retry running the function
            in case of an exception.

    """
    def __init__(self, function, *args, max_retry=3):
        self.function = function
        self.args = args
        self.retry_count = 0
        self.max_retry = max_retry

    def run(self):
        self.start_time = datetime.datetime.now()
        try:
            self.function(*self.args)
        except Exception as e:
            logger.error("Error running task {}".format(self.function.__name__))
            logger.error(e)
            if self.retry_count < self.max_retry:
                self.retry_count += 1
                self.run()
            else:
                raise e
        self.end_time = datetime.datetime.now()

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_duration(self):
        return self.end_time - self.start_time




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
            logger.info("state changed from {} to {}".format(self.previous_state, self.state))
        if self.state in self.state_dict:
            logger.info("state match found for {}".format(self.state))
            self.state_task = self.state_dict[self.state]
            for task in self.state_task:
                logger.info("Running task {}".format(task.__class__.__name__))
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


# add a scehduler that can run the Orchesdtrator at regulat itme intervals


# rewrite the loop of the Scheduler so that it runs in a thread
class Scheduler():
    """
    This is a class to schedule the polling of the state of the jobs.

    Attributes:
        orchestrator: The orchestrator object that is used to poll the state of the jobs.
        interval: The interval in seconds between each poll.

    """
    def __init__(self, orchestrator, interval):
        self.orchestrator = orchestrator
        self.interval = interval
        
        print("Polling thread created")
        self._running = True
        self.thread = threading.Thread(target=self.polling_loop, args =(lambda : self._running, ))

    def run(self):
        self.thread.start()
        

    def polling_loop(self, _running):
        while self._running:
            self.orchestrator.poll_state()
            time.sleep(self.interval)

    def terminate(self):
        self._running = False





# create an abstract class StatePoller that polls the state of the API and returns it
class StatePoller:
    def __init__(self):
        self.state = None

    def poll_state(self):
        return self.state




# create a MockStatePoller class that mocks the state of the API and returns it
class MockStatePoller(StatePoller):
    def __init__(self):
        super().__init__()
        self.state = "state1"

    def poll_state(self):
        self.state = random.choice(["state1", "state2", "state3", "state4", "state5"])
        return self.state

# create an OrchestrationService that take a state / task dictionary as input, the poller,  an interval, set ups an a orchestrator and scheduler and runs it
class OrchestrationService:
    def __init__(self, state_dict, state_poller, interval):
        self.state_dict = state_dict
        self.state_poller = state_poller
        self.interval = interval
        self.scheduler = None

    def run(self):
        orchestrator = Orchestrator(self.state_poller, self.state_dict)
        self.scheduler = Scheduler(orchestrator, self.interval)
        self.scheduler.run()
        

    def stop(self):
        self.scheduler.terminate()






# create an AppianPoller, with in parameter appian api url and api key, with a method that does a request on the api and returns the state
class AppianStatePoller(StatePoller):
    def __init__(self, appian_url, appian_api_key):
        super().__init__()
        self.appian_url = appian_url
        self.appian_api_key = appian_api_key

    def poll_state(self):
        import requests
        import json

        headers = {
            'Authorization': 'appian_api_key',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.get(self.appian_url, headers=headers)

        if response.status_code == 200:
            self.state = json.loads(response.content)["state"]
            return self.state
        else:
            raise Exception("Error getting state from Appian")



# create a function parseappian response that takes a response from the appian api and returns the state
def parse_appian_response(response):
    import json
    return json.loads(response.content)["state"]


# create a class AppianStatePoller that takes a url and an api key and uses a provided parser function to return the state
class AppianStatePoller(StatePoller):
    def __init__(self, appian_url, appian_api_key, parse_function):
        super().__init__()
        self.appian_url = appian_url
        self.appian_api_key = appian_api_key
        self.parse_function = parse_function

    def poll_state(self):
        import requests
        import json

        headers = {
            'Authorization': 'appian_api_key',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = requests.get(self.appian_url, headers=headers)

        if response.status_code == 200:
            self.state = self.parse_function(response)
            return self.state
        else:
            raise Exception("Error getting state from Appian")



# create a mock parse_appian_response function for testing
def mock_parse_appian_response(response):
    return {'TEST_STATE'}


# test the poll_state method of AppianStatePoller with the mock_parse_appian_response function
def test_poll_state():
    mock_poller = AppianStatePoller("https://www.appian.com", "appian_api_key", mock_parse_appian_response)
    assert mock_poller.poll_state() == "TEST_STATE"

# create a pytest of the orchestration service
def test_orchestration_service():
    mock_poller = AppianStatePoller("https://www.appian.com", "appian_api_key", mock_parse_appian_response)
    mock_state_dict = {
        "state1": [Task(print, "state1")],
        "state2": [Task(print, "state2")],
        "state3": [Task(print, "state3")],
        "state4": [Task(print, "state4")],
        "state5": [Task(print, "state5")]
    }
    mock_service = OrchestrationService(mock_state_dict, mock_poller, 1)
    mock_service.run()
    time.sleep(2)
    mock_service.stop()


# create a test with MockStatePoller
def test_orchestration_service_with_mock_poller():
    mock_poller = MockStatePoller()
    mock_state_dict = {
        "state1": [Task(print, "state1")],
        "state2": [Task(print, "state2")],
        "state3": [Task(print, "state3")],
        "state4": [Task(print, "state4")],
        "state5": [Task(print, "state5")]
    }
    mock_service = OrchestrationService(mock_state_dict, mock_poller, 1)
    mock_service.run()
    time.sleep(2)
    mock_service.stop()


test_orchestration_service_with_mock_poller()

class Task:
    def __init__(self, function, *args):
        self.function = function
        self.args = args
        self.retry_count = 0
        self.max_retry = 3

    def run(self):
        self.start_time = datetime.datetime.now()
        try:
            self.function(*self.args)
        except Exception as e:
            logger.error("Error running task {}".format(self.function.__name__))
            logger.error(e)
            if self.retry_count < self.max_retry:
                self.retry_count += 1
                self.run()
            else:
                raise e
        self.end_time = datetime.datetime.now()

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_duration(self):
        return self.end_time - self.start_time




# modify class Task so that max_retry is an optional parameter
class Task:
    def __init__(self, function, *args, max_retry=3):
        self.function = function
        self.args = args
        self.retry_count = 0
        self.max_retry = max_retry

    def run(self):
        self.start_time = datetime.datetime.now()
        try:
            self.function(*self.args)
        except Exception as e:
            logger.error("Error running task {}".format(self.function.__name__))
            logger.error(e)
            if self.retry_count < self.max_retry:
                self.retry_count += 1
                self.run()
            else:
                raise e
        self.end_time = datetime.datetime.now()

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_duration(self):
        return self.end_time - self.start_time

