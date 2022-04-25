"""  aclu/acluUtils.py 
generic utils that use typer
they're here so any clu can use them 
"""

import os
import inspect 
import json 
import typer
from typing import List, Dict 

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
def printLongList(data: List[object], pageSize: int = 7) -> str:
    """
    this is used to print objects in a list in pages
    after each page is printed, ask how to proceed.
    """
    idx = 0
    datalen = len(data) 
    typer.echo(f'there are {datalen} items, printing {pageSize} items per page')
    while idx < datalen:
        typer.echo(f'item {idx}: {data[idx]}')
        idx += 1
        if pageSize > 0 and  idx % pageSize == 0:  
            try:
                cmd = typer.prompt('q to quit, c to continue, a to print all remaining items, b to show all items in browser', default='c', show_default=True) 
            except (TypeError, ValueError) as exc:
                typer.echo(f'something strange happened. error is {exc}')
            else:
                if cmd.lower() == 'q': return 'q' 
                elif cmd.lower() =='a': pageSize = 0 
                elif cmd.lower() == 'b': return 'b'
                # else assume anything else means continue with printing pages 
    # normal exit after all items have been printed 
    return 'c' 

#######
# special read config to allow for comments in json file 
##
def readJsonConfigWithComments(configFile: str) -> Dict:
    jstr = ''
    try:
        with open(configFile, 'r') as f:
            for line in f.readlines():
                ## ignore any comment lines, starting with //  
                if not line.lstrip().startswith('//'): jstr += line 
        ## we have the text, now try to turn it into an object to return 
        return json.loads(jstr)
    except Exception as ex:
            typer.echo(f'failed to parse json config in file {configFile}.  error: {ex}')
            return None 

#######
def getModuleDir() -> str:
    """
    TODO: this is a total hack and needs to change 
    this returns the absolute path of the module that called  getModuleDir()
    I'm using this to get the path to templates directories in various modules 
    which I need for the jinja FileSystemLoader 
    TODO: I should be using proper resource management for templates directories 
    """
    abspath = os.path.abspath(inspect.getabsfile(inspect.currentframe().f_back))
    dirname, filename = os.path.split(abspath)
    return dirname 

#######
def storeLocals(cmd: str, parms: Dict) -> Dict:
    """
    storing the local variables, including their values, on entering a commands function, 
    enables more generic templating code 
    we need to exclude the typer.Context parameter though if it exists in locals 
    """
    pc = parms.copy()
    for k,v in pc.items():
        if 'Context' in str(type(v)): 
            pc.pop(k)
            break 
    locs = {'command': cmd, 'parameters': pc}
    # typer.echo(json.dumps(locs, indent=4))


## end of file 