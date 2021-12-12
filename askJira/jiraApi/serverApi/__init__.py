
import typer

app = typer.Typer()
jiraServerBaseUrl = 'https://jira.ringcentral.com/rest/api/latest/'

##
# any @app.command() functions in modules in this package 
# need to be imported here
##
from .dashboards import dashboards 

