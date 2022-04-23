""" aclu/searchjira/cli.py 
"""

import typer
from typing import List, Dict 

from . import app
import ui 
from jiraApi import JiraApi 
from acluUtils import printLongList, getModuleDir  

""" help strings that are used in multiple commands """ 
searchStringsHelp = "strings to search for in resource name, default is match any of the strings"
idsHelp = "search strings are IDs of resources, much faster if you know what you're looking for"
containsAllHelp = "flag to indicate match all search words, default is to match any search word. "
caseSensitiveHelp = "flag to make search case sensitive"
showInBrowserHelp = "show search results in your default web browser"


#######
def showInBrowser(props: Dict, template: str) -> None:
    ui.initEnv([getModuleDir() + '/templates'])
    ui.openPage(props, template)


#######
@app.command()
def dashboards(ctx: typer.Context,
        searchstrings: List[str] = typer.Argument(..., help=searchStringsHelp),
        ids: bool = typer.Option(False, "-i", "--ids", help=idsHelp),
        containsall: bool = typer.Option(False, "-a", "--all", help=containsAllHelp),
        casesensitive: bool = typer.Option(False, "-c", "--casesensitive", help=caseSensitiveHelp),
        showinbrowser: bool = typer.Option(False, "-b", "--browser", help=showInBrowserHelp)
) -> None:
    jirapi = ctx.obj 
    searchstrings = list(set(searchstrings))
    if ids:
        ## dabrds = [db if db else {id: "Does Not Exist"} for id in searchstrings if (db := jirapi.getDashboard(id)) or True]
        dabrds = [db for id in searchstrings if (db := jirapi.getDashboard(id)) or (db := {id: "Does Not Exist"} if not db else db)]
    else:
        dabrds = jirapi.findDashboards(searchstrings, containsall, casesensitive)
    if showinbrowser or printLongList(dabrds) == 'b':
        typer.echo('opening new tab in your default browser')
        props ={
            'title': ' '.join(searchstrings)
        }
        showInBrowser(props, 'dashboards.html')


#######
@app.command()
def boards(ctx: typer.Context,
        searchstrings: List[str] = typer.Argument(..., help=searchStringsHelp),
        ids: bool = typer.Option(False, "-i", "--ids", help=idsHelp),
        containsall: bool = typer.Option(False, "-a", "--all", help=containsAllHelp),
        casesensitive: bool = typer.Option(False, "-c", "--casesensitive", help=caseSensitiveHelp),
        showinbrowser: bool = typer.Option(False, "-b", "--browser", help=showInBrowserHelp)
) -> None:
    jirapi = ctx.obj 
    searchstrings = list(set(searchstrings))
    if ids:
        ## brds = [brd if brd else {id: "Does Not Exist"} for id in searchstrings if (brd := jirapi.getBoard(id)) or True]
        brds = [brd for id in searchstrings if (brd := jirapi.getBoard(id)) or (brd := {id: "Does Not Exist"} if not brd else brd)]
    else:
        brds = jirapi.findBoards(searchstrings, containsall, casesensitive)
    retOpt = printLongList(brds)
    if retOpt == 'b':
        typer.echo('soon...')


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
        configfile: str = typer.Option(None, "-c", "--configfile"), 
        templatedirs: str = typer.Option(None, "-t", "--templatedirs"),
        jira_user: str = typer.Option(..., 
            "-u", "--jirauser", envvar="JIRA_USER",
            prompt="Please enter your jira username: "),
        jira_pw: str = typer.Option(..., 
            "-p", "--jirapw", envvar="JIRA_PW",
            prompt="Please enter your jira password: ",
            confirmation_prompt=True, hide_input=True),
        jira_base_url: str = typer.Option(..., 
            "-r", "--jiraurl", envvar="JIRA_BASE_URL",
            prompt="Please enter the base URL for Jira: ",)
) -> None: 
    if configfile:
        typer.echo(f'using config file: {configfile}')
    if templatedirs:
        typer.echo(f'using template directories: {templatedirs}')
    # ctx.obj is used to pass information to commands 
    ctx.obj = JiraApi(jira_user, jira_pw, jira_base_url )


## end of file 