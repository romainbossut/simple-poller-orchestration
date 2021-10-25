# set up a logger and loggin capability
import logging
import time

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

# create a handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

import orchestration as orch
import pollers as pol


def test_orchestration_service_with_mock_poller():
    mock_poller = pol.MockStatePoller()
    mock_state_dict = {
        "state1": [orch.Task(print, "state1")],
        "state2": [orch.Task(print, "state2")],
        "state3": [orch.Task(print, "state3")],
        "state4": [orch.Task(print, "state4")],
        "state5": [orch.Task(print, "state5")]
    }
    mock_service = orch.OrchestrationService(mock_state_dict, mock_poller, 1)
    mock_service.run()
    time.sleep(5)
    mock_service.stop()


test_orchestration_service_with_mock_poller()
