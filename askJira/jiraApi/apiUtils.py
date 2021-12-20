"""
some utilities mostly here to not clutter up other code with try except stuff
also code for structures common across different Atlassian APIs 
"""

import typer 
import json 
from typing import List, Dict

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


## end of file 