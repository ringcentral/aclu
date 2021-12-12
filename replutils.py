"""
some basic stuff to use as I'm poking around in the python repl 
go to the end of the file to see the short names to import
"""

import os 
import requests 
import json 


jiraUser = os.getenv('JIRA_USER')
jiraPw = os.getenv('JIRA_PW')
jiraCreds = (jiraUser, jiraPw)
jiraBaseUrl = 'https://jira.ringcentral.com/rest/api/latest/' 
agileBaseUrl = 'https://jira.ringcentral.com/rest/agile/latest/' 


class JiraGet:
    def __call__(self, resource: str) -> object:
        return requests.get(jiraBaseUrl + resource, auth=jiraCreds)

class AgileGet:
    def __call__(self, resource: str) -> object:
        return requests.get(agileBaseUrl + resource, auth=jiraCreds)

def prettyPrintJsonString(payload: str) -> None:
    """
    pretty print a string representing a JSON object.
    I didn't like the way the pprint builtin works
    """
    try:
        print(json.dumps(json.loads(payload), indent=4))
    except Exception as e:
        print(f'payload was not valid json: {e}')

def printObjectFirstLevel(ob: object) -> None:
    try:
        for k,v in ob.items():
            print(f'key {k} has value with type {type(v)}')
    except Exception as ex:
        print(f'something bad happened while trying to print object. errer: {ex}')


server = JiraGet() 
agile = AgileGet()
ppjs = prettyPrintJsonString 
pofl = printObjectFirstLevel 


## end of file 