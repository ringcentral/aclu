"""
some utilities mostly here to not clutter up other code with try except stuff
also code for structures common across different Atlassian APIs 

And moved requests here in case I want to change 
how GETs are done in the future.
"""

import requests 
import typer 
import json 
from typing import List, Dict, Tuple 

#######
def getObjectFromJsonString(jstr: str) -> object:
    try:
        return json.loads(jstr)
    except Exception as ex:
        typer.echo(f'not a JSON string.  error: {ex}')
        typer.echo(f'beginning of string is <{jstr[:16]}>')
        return None 


#######
# if search strings exists, 
# compare each string against the name of each value object
# if there's a match (including substring), 
# add that value object to the set of value objects to return 
# 
# remeember if there are multiple search strings, more than one could match the name of a value
# we could use a set and not track whether a value has been added to the list, 
# but the values are dicts thus cannot be added to sets
## 
def searchNamesInValues(values: list[object], searchList: List[str] = None, caseSensitive: bool = False, printNames: bool = False) -> List[Dict]:
    ret = []
    for val in values:
        name = val['name']
        origName = name ## use this for print in case name gets lowered later 
        added = False 
        if printNames:
            typer.echo(origName)
        if searchList:
            if not caseSensitive: name = name.lower()
            for sstr in searchList:
                origSstr = sstr  # in case sstr gets lowered 
                if not caseSensitive: sstr = sstr.lower()
                if sstr in name:
                    typer.echo(f'string {origSstr} is part of value named {origName}')
                    if not added:
                        ret.append(val)
                        added = True 
    return ret 


#######
def getOption(choices: List[str]) -> int:
    """ 
    take in a list of strings,
    each represents a choice.
    return index of the string for the choice chosen 
    """
    while True:  ## hacked do while 
        idx = 0
        for choice in choices:
            idx += 1
            typer.echo(f'{idx} -- {choice}')
        try:
            option = int(typer.prompt('choose from the list'))
        except (TypeError, ValueError) as exc:
            typer.echo(f'you buggered it, try again. error is {exc}')
        else:
            if option > 0 and option <= idx: return option - 1  
            else: typer.echo('option is not in range, try again')

#######
# I should probably create a class to encapsulate the GET requests 
# for now, being lazy with file scope 
jiraCreds = None 

#######
def setJiraCreds(credentials: tuple) -> None:
    global jiraCreds
    jiraCreds = credentials 

#######
def getResource(url: str, convertPayload: bool = False) -> Tuple[object, object]:
    """
    only return the resource if the status_code is 2xx.
    this eliminates having to check in the calling methods.
    And allow the caller to ask for the payload to be converted to an object.
    this can make for cleaner code for the caller.
    And the caller should know whether the payload should be JSON text.
    Return is the Response object and the payload text converted to an object
    if convertPayload was true, else return None for the payload object
    if resp was not ok, return None for both objects 
    """
    try:
        resp = requests.get(url, auth = jiraCreds)
        if resp != None and resp.ok: 
            if convertPayload: return  resp, getObjectFromJsonString(resp.text)
            else: return resp, None  
        else:
            ## okay, we could be here because resp was None and maybe I should fix that.
            ## we're in a try block though so I'm going to let it ride for now.
            typer.echo(f'query to {url}, was not okay.  error: {resp.text}')
    except Exception as  exec:
        typer.echo(f'Caught exception on query to {url}.  Exception: {exec}')
    return None, None  


#######
def getResourcesFromPayload(payload: object) -> List[Dict]:
    """
    we need the list of resources.  this is where the pagination is inconsistent.
    sometimes the key name is 'values', sometimes its named based on the type of resources in the list
    in all cases though, it's the only list in the payload.
    so find the list item in the payload, and that should be the resources  
    """
    for v in payload.values():
        if isinstance(v, list): return v
    return None 


#######
def getUrlForNextPage(resourceUrl: str, payload: object) -> str:
    """
    This is the other place of inconsistency across the paginated resources.
    some meta data has an isLast boolean property, 
    some has a next string property for the next URL to use.
    And I've seen cases with neither but a value of 0 for the total property 
    and a list of resources of length 0 indicating there are no more pages.
    This function is initially based on those observations.
    Ran in to a problem with dashboards in the server platform API
    Dashboards uses a next URL to indicate there is another page.
    Once the startAt has exceeded the total, there is no longer a next property in the meta data.
    But in this generic function, how to know that is different than a resource that should have an isLast parameter but doesn't?
    Anyway, that's why the check for startAt > total.
    """
    startAt = payload.get('startAt', None)
    maxResults = payload.get('maxResults', None)
    total = payload.get('total', None)
    isLast = payload.get('isLast', None)
    next = payload.get('next', None)
    typer.echo(f'started at: {startAt}, max results: {maxResults}, total available: {total}, is last: {isLast}, next is {"NOT None" if next != None else None}')
    ## now the logic.
    ## these checks represent what I have seen so far
    if next: return next
    if isLast or (total == 0) or (startAt > total): return None 
    ## else, we need to construct the next url based on the base and properties from the payload 
    return f'{resourceUrl}?startAt={startAt + maxResults}&maxResults={maxResults}'


#######
def getPaginatedResources(resourceUrl: str, pageSize: int = 50, searchList: List[str] = None, caseSensitive: bool = False, printNames: bool = False, answerYes: bool = False) -> List[Dict]:
    """
    this is the starting point to getting the list of resources for a paginated resource 
    it takes the base URL of the resource and desired page size.
    and the various options and flags too filter or act on the resource paging.
    it returns the list of resources, if any found, else empty list.
    """
    resources = []
    nextUrl = f'{resourceUrl}?maxResults={pageSize}'
    while nextUrl:
        _, payload = getResource(nextUrl, convertPayload=True)
        if payload == None:
            typer.echo(f'no payload for url {nextUrl}?!?  Very odd')
            return resources 
        ## else carry on with the payload 
        currentResources = getResourcesFromPayload(payload)
        if searchList or printNames:
            ## might trim the list based on search strings, or maybe just print the names of the resources 
            currentResources = searchNamesInValues(currentResources, searchList, caseSensitive, printNames)
        resources += currentResources 
        ## now determine if we should get the next page
        ## firstly, is there a next page?
        nextUrl = getUrlForNextPage(resourceUrl, payload)
        if nextUrl and (answerYes or typer.confirm('get next page?')):
            pass
        else:
            break
    ## either got all the pages, or all the pages the user wanted 
    return resources 


## end of file 