"""
some utilities mostly here to not clutter up other code with try except stuff
also code for structures common across different Atlassian APIs 

And moved requests here in case I want to change 
how GETs are done in the future.
"""

import logging 
logger = logging.getLogger(__name__)

import requests 
import json 
from typing import TypeVar, List, Dict, Tuple 
StrOrDict = TypeVar('StrOrDict', str, Dict) 


#######
def getObjectFromJsonString(jstr: str) -> object:
    try:
        return json.loads(jstr)
    except Exception as ex:
        logger.exception(f'not a JSON string.  beginning of string is <{jstr[:16]}>')
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
def searchNamesInValues(values: list[Dict], searchList: List[str], caseSensitive: bool = False) -> List[Dict]:
    ret = []
    if values is None or searchList is None:
        logger.warning('values and/or searchList is None')
    else:
        for val in values:
            name = val['name']
            origName = name ## use this for print in case name gets lowered later 
            if not caseSensitive: name = name.lower()
            added = False 
            for sstr in searchList:
                origSstr = sstr  # in case sstr gets lowered 
                if not caseSensitive: sstr = sstr.lower()
                if sstr in name:
                    logger.info(f'string {origSstr} is part of value named {origName}')
                    if not added:
                        ret.append(val)
                        added = True 
    return ret 


#######
# I should probably create a class to encapsulate the GET requests 
# for now, being lazy with file scope 
jiraCreds = None 
def setJiraCreds(credentials: tuple) -> None:
    global jiraCreds
    jiraCreds = credentials 

#######
def getResource(url: str, convertPayload: bool = False) -> Tuple[requests.Response, Dict]:
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
        logger.debug(f'getting {url}, convertPayload: {convertPayload}')
        resp = requests.get(url, auth = jiraCreds)
        if resp is None : return (None, None)
        if not resp.ok:
            logger.info(f'query to {url}, returned status code: {resp.status_code}')
            return None,None
        if convertPayload: return  resp, getObjectFromJsonString(resp.text)
        else: return resp, None  
    except Exception as  exec:
        logger.exception(f'Caught exception on query to {url}.')
    return None, None  


#######
def getResourcesFromPayload(payload: Dict) -> List[Dict]:
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
def getUrlForNextPage(resourceUrl: str, payload: Dict) -> str:
    """
    This is a big place of inconsistency across the paginated resources.
    some meta data has an isLast boolean property, 
    some has a next string property for the next URL to use.
    And I've seen cases with neither but a value of 0 for the total property 
    and a list of resources of length 0 indicating there are no more pages.
    This function was initially based on those observations.
    the built up over time as I ran in to more differences 
    Ran in to a problem with dashboards in the server platform API
    Dashboards uses a next URL to indicate there is another page.
    Once the startAt has exceeded the total, there is no longer a next property in the meta data.
    But in this generic function, how to know that is different than a resource that should have an isLast parameter but doesn't?
    Anyway, that's why the check for startAt > total.
    Ran in to an issue with getting issues on a sprint.
    There was no 'next' field and no 'isLast' field.
    There is a 'total though and 
    a list of resources with len lesss than maxResults
    I've also seen this case but no 'total' property.
    I need to get the len of the list of resources and 
    if that is less than maxResults, nextUrl should be None
    """
    startAt = payload.get('startAt', None)
    maxResults = payload.get('maxResults', None)
    total = payload.get('total', None)
    isLast = payload.get('isLast', None)
    next = payload.get('next', None)
    numResources = len(getResourcesFromPayload(payload))
    logger.info(f'started at: {startAt}, max results: {maxResults}, total available: {total}, numResources: {numResources}, is last: {isLast}, next is {"NOT None" if next != None else None}')
    ## now the logic.
    if next: return next
    if isLast: return None 
    if total and ((total == 0) or (startAt > total)): return None 
    if numResources < maxResults: return None 
    ## else, we need to construct the next url based on the base and properties from the payload 
    return f'{resourceUrl}?startAt={startAt + maxResults}&maxResults={maxResults}'


#######
def getPaginatedResources(resourceUrl: str, pageSize: int = 50, searchList: List[str] = None, caseSensitive: bool = False) -> List[Dict]:
    """
    this is the starting point to getting the list of resources for a paginated resource 
    it takes the base URL of the resource and desired page size.
    And the list of strings to search on to filter the list. 
    it returns the list of resources, if any found, else empty list.
    """
    resources = []
    nextUrl = f'{resourceUrl}?maxResults={pageSize}'
    while nextUrl:
        resp, payload = getResource(nextUrl, convertPayload=True)
        if payload == None:
            logger.warning(f'no payload for url {nextUrl}?!? status code was {resp.status_code}')
            return resources 
        ## else carry on with the payload 
        currentResources = getResourcesFromPayload(payload)
        if searchList:
            ## might trim the list based on search strings
            currentResources = searchNamesInValues(currentResources, searchList, caseSensitive)
        resources += currentResources 
        ## is there a next page?
        nextUrl = getUrlForNextPage(resourceUrl, payload)
    return resources 


## end of file 