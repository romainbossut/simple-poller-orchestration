# create a class orchestrator, that polls a state from an api, has a dictionary of possible states linked to a Task and run them
import threading
import datetime
import time
import random









# add a scehduler that can run the Orchesdtrator at regulat itme intervals


# rewrite the loop of the Scheduler so that it runs in a thread

















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
