""" aclu/roadmap/cli.py 
"""

import typer 

from . import app
import ui 
import jiraApi 


@app.callback(invoke_without_command=True)
def main(
        configfile: str = typer.Option(None, "-c", "--configfile"),
        templatedirs: str = typer.Option(None, "-t", "--templatedirs")
) -> None:
    if configfile:
        typer.echo(f'using config file: {configfile}')
    if templatedirs:
        typer.echo(f'using template directories: {templatedirs}')
    typer.echo("that's it for the roadmap.")


## end of file 