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


# function that draws a chart of the state_dict
def draw_state_dict_chart(state_dict):
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()

    for state in state_dict:
        G.add_node(state)
        for task in state_dict[state]:
            G.add_node(task.get_function().__name__)
            G.add_edge(state, task.get_function().__name__)

    nx.draw(G, with_labels=True)
    plt.show()


# function that draws a chart of the state_dict
def draw_state_dict_chart_with_state_inputs(state_dict):
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()

    for state in state_dict:
        G.add_node(state)
        for task in state_dict[state]:
            G.add_node(task.get_function().__name__)
            G.add_edge(state, task.get_function().__name__)

    nx.draw(G, with_labels=True)
    plt.show()


# draw the following dict
import matplotlib.pyplot as plt
mock_state_dict = {
        "state1": [orch.Task(print, "state1"), orch.Task(plt.show, "state1 second print")],
        "state2": [orch.Task(print, "state2")],
        "state3": [orch.Task(print, "state3")],
        "state4": [orch.Task(print, "state4")],
        "state5": [orch.Task(print, "state5")]
    }
draw_state_dict_chart(mock_state_dict)

