""" aclu/searchjira/__init__.py 
"""

import typer
app = typer.Typer()
app_name = "searchjira"

# any @app functions need to be inmported here
from searchjira.cli import main


def run():
    app(prog_name=app_name)

## end of file