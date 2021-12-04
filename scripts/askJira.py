#!/usr/bin/env python

import typer 
import requests 
import utils 


app = typer.Typer() 
jiraCreds = None 
jiraBaseUrl = 'https://jira.ringcentral.com/rest/api/latest/'


#######
def printDashboardNames(dbs: list) -> None:
    for db in dbs:
        typer.echo(db['name'])


#######
def processDashboardResponse(resp: object) -> str:
    typer.echo('processing dashboard response')
    next = None
    dbo = utils.getObjectFromJsonString(resp.text)
    if dbo != None:
        startAt = dbo['startAt']
        maxResults = dbo['maxResults']
        total = dbo['total']
        next = dbo['next']
        typer.echo(f'started at: {startAt}, max results: {maxResults}, total available: {total}')
        typer.echo(f'issue next query with URL: {next}')
        printDashboardNames(dbo['dashboards'])
    ## this is not broken indentation, next was initiated to None 
    return next


#######
@app.command(name='dbs')
def dashboards() -> None:
    typer.echo('looking through the dashboards')
    resp = requests.get(jiraBaseUrl+ 'dashboard?maxResults=50', auth = jiraCreds)
    processDashboardResponse(resp)


#######
@app.callback(invoke_without_command=True)
def main(
        jira_user: str = typer.Option(..., 
            "-u", "--jirauser", envvar="JIRA_USER", 
            prompt="Please enter your jira username: "),
        jira_pw: str = typer.Option(..., 
            "-p", "--jirapw", envvar="JIRA_PW", 
            prompt="Please enter your jira password: ", 
            confirmation_prompt=True, hide_input=True)
):
    typer.echo(f'Hello Jira User: {jira_user}') 
    global jiraCreds 
    jiraCreds = (jira_user, jira_pw) 


if __name__ == "__main__":
    app()


    ## end of file 