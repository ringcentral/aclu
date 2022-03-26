"""
utils that use typer
"""

import typer
from typing import List


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