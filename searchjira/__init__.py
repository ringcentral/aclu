""" aclu/searchjira/__init__.py 
"""

import typer
app = typer.Typer()
app_name = "searchjira"

from .cli import main


def run():
    app(prog_name=app_name)

## end of file