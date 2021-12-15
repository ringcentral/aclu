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
        added = False 
        if printNames:
            typer.echo(name)
        if searchList:
            if not caseSensitive: name = name.lower()
            for sstr in searchList:
                if not caseSensitive: sstr = sstr.lower()
                if sstr in name:
                    typer.echo(f'string {sstr} is part of value named {name}')
                    if not added:
                        ret.append(val)
                        added = True 
    return ret 


## end of file 