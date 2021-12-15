
import typer

app = typer.Typer()

jiraAgileBaseUrl = 'https://jira.ringcentral.com/rest/agile/latest/' 

##
# any @app.command() functions in modules in this package 
# need to be imported here
##
from .boards import boards 


## end of file 