""" aclu/roadmap/__init__.py 
"""

import typer
app = typer.Typer()
app_name = "roadmap"

# any @app functions need to be inmported here
from roadmap.cli import main


def run():
    app(prog_name=app_name)

# end of file