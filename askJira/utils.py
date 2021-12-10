"""
some utilities mostly here to not clutter up other code with try except stuff
"""

import typer 
import json 

#######
def getObjectFromJsonString(jstr: str) -> object:
    try:
        return json.loads(jstr)
    except Exception as ex:
        typer.echo(f'not a JSON string.  error: {ex}')
        typer.echo(f'beginning of string is <{jstr[:16]}>')
        return None 

        ## end of file 