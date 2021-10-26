# set up a logger and loggin capability
import log
import time


import orchestration as orch
import pollers as pol


def test_orchestration_service_with_mock_poller():
    mock_poller = pol.MockStatePoller()
    mock_state_dict = {
        "state1": [orch.Task(print, "state1"), orch.Task(print, "state1 second print")],
        "state2": [orch.Task(print, "state2")],
        "state3": [orch.Task(print, "state3")],
        "state4": [orch.Task(print, "state4")],
        "state5": [orch.Task(print, "state5")]
    }
    mock_service = orch.OrchestrationService("Test Service", mock_state_dict, mock_poller, 1)
    mock_service.run()
    time.sleep(5)
    mock_service.stop()


test_orchestration_service_with_mock_poller()
