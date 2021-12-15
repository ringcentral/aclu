"""
some basic stuff to use as I'm poking around in the python repl 
go to the end of the file to see the short names to import
"""

import os 
import sys 
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
            # only print values for strings, bools, and ints.
            # print length of lists 
            # else print the type and memory size 
            if isinstance(v, (int, str, bool)):
                print(f'key {k}: value {v}')
            elif isinstance(v, list):
                print(f'key {k}: is list with length {len(v)}')
            else:
                print(f'key {k}: has type {type(v)} and memory size {sys.getsizeof(v)}')
    except Exception as ex:
        print(f'something bad happened while trying to print object. errer: {ex}')

def printResponseFirstLevel(resp):
    try:
        printObjectFirstLevel(json.loads(resp.text)) 
    except Exception as ex:
        print(f'something bad happened while trying to print response. errer: {ex}')

server = JiraGet() 
agile = AgileGet()
ppjs = prettyPrintJsonString 
pofl = printObjectFirstLevel 
prfl = printResponseFirstLevel 

# cut/n/paste this into the repl:
# from replutils import server, agile, ppjs, pofl, prfl 

## end of file 