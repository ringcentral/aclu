#!/usr/bin/env python

import typer 
import requests 
import utils 
from typing import List, Optional  


app = typer.Typer() 
jiraBaseUrl = 'https://jira.ringcentral.com/rest/api/latest/'


#######
def processDashboards(dbs: list, searchList: List[str] = None, printNames: bool = False) -> None:
    for db in dbs:
        name = db['name']
        if printNames:
            typer.echo(name)
        if searchList:
            for sstr in searchList:
                if sstr.lower() in name.lower():
                    typer.echo(f'string {sstr} is part of dashboard name {name}')


#######
def processDashboardResponse(resp: object, searchList: List[str] = None, printNames: bool = False, answerYes: bool = False) -> str:
##     typer.echo('processing dashboard response'),
    next = None
    dbo = utils.getObjectFromJsonString(resp.text)
    if dbo != None:
        startAt = dbo['startAt']
        maxResults = dbo['maxResults']
        total = dbo['total']
        typer.echo(f'started at: {startAt}, max results: {maxResults}, total available: {total}')
        if searchList or printNames:
            processDashboards(dbo['dashboards'], searchList, printNames)
        if answerYes or  typer.confirm('Continue to the next block of dashboards?'):
            ## can't use {} as next doesn't exist if on last page 
            next = dbo.get('next', None)
            ## typer.echo(f'issue next query with URL: {next}')
    ## this is not broken indentation, next was initiated to None 
    return next


#######
dbsHelp =     """
    dbs is short for dashboards \n
    must use either -s or -n, or both. \n
    multiple -s options will result in finding dashboard with names containing any of those strings (OR'd) \n
    if you use -y, you probably want a larger pageSize  \n
    if you use -n, you probably want a smaller pageSize  \n
    """

@app.command(name='dbs', help=dbsHelp)
def dashboards(ctx: typer.Context, 
        searchList: Optional[List[str]] = typer.Option(None, "-s", "--search", help="use multiple -s options to search for multiple strings."),   
        printNames: bool = typer.Option(False, "-n", "--names", help="print the name of each dashboard."),
        pageSize: int = typer.Option(50, "-p", "--pageSize", help="how many dashboards to retrieve on each GET."),
        answerYes: bool = typer.Option(False, "-y", "--yes", help="don't ask to continue after each page, just do it!")
) -> None:
    jiraUser, jiraPw, jiraUrl = ctx.obj
    typer.echo(f'looking at dashboards for user: {jiraUser}')
    if searchList: 
        typer.echo(f'Search dashboards for any of {searchList}')
    elif printNames:
        typer.echo('print names of dashboards')
    else:
        typer.echo('either search or print, otherwise, why are you here?')
        return
    resp = requests.get(jiraUrl + f'dashboard?maxResults={pageSize}', auth = (jiraUser, jiraPw))
    while (next := processDashboardResponse(resp, searchList, printNames, answerYes)) != None:
        resp = requests.get(next, auth = (jiraUser,jiraPw))


#######
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, 
        jira_user: str = typer.Option(..., 
            "-u", "--jirauser", envvar="JIRA_USER", 
            prompt="Please enter your jira username: "),
        jira_pw: str = typer.Option(..., 
            "-p", "--jirapw", envvar="JIRA_PW", 
            prompt="Please enter your jira password: ", 
            confirmation_prompt=True, hide_input=True)
):
    typer.echo(f'Hello Jira User: {jira_user}') 
    ctx.obj = (jira_user, jira_pw, jiraBaseUrl) 


if __name__ == "__main__":
    app()


    ## end of file 