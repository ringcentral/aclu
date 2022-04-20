"""  aclu/replutils.py 
some basic stuff to use as I'm poking around in the python repl 
"""

from jiraApi import JiraApi 
ja = JiraApi()

"""
below here is stuff I wwrote before creating the JiraApi class
I'm leaving it as it's still a decent way of querying the Jira API
if there's something not (yet) supported in JiraApi
"""

import os 
import sys 
import requests 
import json 

jiraUser = os.getenv('JIRA_USER')
jiraPw = os.getenv('JIRA_PW')
jiraBaseUrl = os.getenv('JIRA_BASE_URL')
jiraCreds = (jiraUser, jiraPw)
serverBaseUrl = f'{jiraBaseUrl}/rest/api/latest' 
agileBaseUrl = f'{jiraBaseUrl}/rest/agile/latest' 

class ServerGet:
    def __call__(self, resource: str) -> object:
        return requests.get(f'{serverBaseUrl}/{resource}', auth=jiraCreds)

class AgileGet:
    def __call__(self, resource: str) -> object:
        return requests.get(f'{agileBaseUrl}/{resource}', auth=jiraCreds)

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
            # only print values for strings, bools, and ints.
            # print length of lists 
            # else print the type and memory size 
            if isinstance(v, (int, str, bool)):
                print(f'key {k}: value {v}')
            ## elif isinstance(v, list):
            elif hasattr(v, '__len__'):
                print(f'key {k}: has type {type(v)}, with length {len(v)}')
            else:
                print(f'key {k}: has type {type(v)} and memory size {sys.getsizeof(v)}')
    except Exception as ex:
        print(f'something bad happened while trying to print object. errer: {ex}')

def printResponseFirstLevel(resp):
    try:
        printObjectFirstLevel(json.loads(resp.text)) 
    except Exception as ex:
        print(f'something bad happened while trying to print response. errer: {ex}')

server = ServerGet() 
agile = AgileGet()
ppjs = prettyPrintJsonString 
pofl = printObjectFirstLevel 
prfl = printResponseFirstLevel 

## end of file 