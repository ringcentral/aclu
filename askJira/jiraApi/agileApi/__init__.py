##
# __init__.py for the agileApi package 
#
# the Jira agile API sits on top of (sort of) the server API.
# The API is based on boards which contain epics and sprints (for scrum boards).
# Epics and sprints are really just a way to associate and manage issues.
# Boards have issues associated with epics and some not associated with epics.
#
# Mostly we'll be using the /agile/latest/board endpoint.
# for a specific board, we will use 
#  - /agile/latest/board/<boardId>/epic/<epicId>/issue
#  - /agile/latest/board/<boardId>/epic/none/issue 
# to get the issues
#
# the main entry to the package is through the boards subcommand under the agile command in askJira.
# If a board is selected to get more info, the boardId related endpoints are querried for details of the board 
##

import typer

app = typer.Typer()

jiraAgileBaseUrl = 'https://jira.ringcentral.com/rest/agile/latest/' 

##
# any @app.command() functions in modules in this package 
# need to be imported here
##
from .boards import boards 


## end of file 