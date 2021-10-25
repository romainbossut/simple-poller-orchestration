# create an AppianPoller, with in parameter appian api url and api key, with a method that does a request on the api and returns the state
from .StatePoller import StatePoller

def parse_appian_response(response):
    import json
    return json.loads(response.content)["state"]


# create a mock parse_appian_response function for testing
def mock_parse_appian_response(response):
    return {'TEST_STATE'}


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


