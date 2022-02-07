#!/usr/bin/env python

import json 
import os.path as path 
import typer
from typing import Dict 
from jiraApi import serverApi
from jiraApi import agileApi 


app = typer.Typer()
app.add_typer(serverApi.app, name='server')
app.add_typer(agileApi.app, name='agile')

#######
# special read config to allow for comments in json file 
##
def readJsonConfigWithComments(configFile: str) -> Dict:
    jstr = ''
    try:
        with open(configFile, 'r') as f:
            for line in f.readlines():
                ## ignore any comment lines, starting with //  
                if not line.lstrip().startswith('//'): jstr += line 
        ## we have the text, now try to turn it into an object to return 
        return json.loads(jstr)
    except Exception as ex:
            typer.echo(f'failed to parse json config in file {configFile}.  error: {ex}')
            return None 

#######
def runBasedOnConfig(configFile: str, jiraUser: str, jiraPw: str) -> None:
    typer.echo(f'using config file {configFile}')
    configObj = readJsonConfigWithComments(configFile)
    if configObj == None:
        typer.echo(f'something is wrong with your config file {configFile}')
        return
    ##
    # we seem to have a valid JSON config, let's do something with it..

#######
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
         config_file: str = typer.Option(None, "-c", "--config", help="JSON formatted config file"),
         jira_user: str = typer.Option(...,
                                       "-u", "--jirauser", envvar="JIRA_USER",
                                       prompt="Please enter your jira username: "),
         jira_pw: str = typer.Option(...,
                                     "-p", "--jirapw", envvar="JIRA_PW",
                                     prompt="Please enter your jira password: ",
                                     confirmation_prompt=True, hide_input=True)
         ) -> None:
    typer.echo(f'Hello Jira User: {jira_user}')
    ## the Context obj is used to pass information to subcommands     
    ctx.obj = (jira_user, jira_pw)
    ## 
    # if there is a config file specified, use that
    # else, let typer do its thing and route to the specified command (which happens by default) 
    if config_file != None:
        runBasedOnConfig(config_file, jira_user, jira_pw)


#######
if __name__ == "__main__":
    app()

    # end of file