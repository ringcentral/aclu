
import typer

app = typer.Typer()
##
# any @app.command() functions in modules in this package 
# need to be imported here
##
from .dashboards import dashboards 

