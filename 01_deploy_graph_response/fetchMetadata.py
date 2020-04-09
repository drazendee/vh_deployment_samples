import requests
import json

# Authenticate yourself with the token
auth_token = '<my-auth-token>'
headers = {'Authorization': 'Token %s' % auth_token}

# Send a request (with the authentication headers) to fetch all executions in a project
# You can get the project ID for example
resp = requests.get('https://app.valohai.com/api/v0/executions/<my-execution-id>/metadata/', headers=headers)

resp.raise_for_status()

with open("metadata.json", "w") as outfile:
    json.dump(resp.json(), outfile, indent=4)