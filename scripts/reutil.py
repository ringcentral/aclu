"""
some basic stuff to use as I'm poking around in the python repl 
"""

import os 
import requests 
import json 


jiraUser = os.getenv('JIRA_USER')
jiraPw = os.getenv('JIRA_PW')
jiraCreds = (jiraUser, jiraPw)
jiraBaseUrl = 'https://jira.ringcentral.com/rest/api/latest/' 

class JiraGet:
    def __call__(self, resource: str) -> object:
        return requests.get(jiraBaseUrl + resource, auth=jiraCreds)

jira = JiraGet() 

def pp(payload: str) -> None:
    try:
        print(json.dumps(json.loads(payload), indent=4))
    except Exception as e:
        print(f'payload was not valid json: {e}')


"""
def pp(payload: str) -> None:
    try:
        o = json.loads(payload)
        formatted = json.dumps(o, indent=4)
        print(formatted)
    except Exception as e:
        print(f'payload was not valid json: {e}')
"""

## end of file 