#!/usr/bin/env python

import typer
import serverApi
import agileApi 


app = typer.Typer()
app.add_typer(serverApi.app, name='server')
app.add_typer(agileApi.app, name='agile')


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
    ## the Context obj is used to pass information to subcommands 
    
    ctx.obj = (jira_user, jira_pw)


#######
if __name__ == "__main__":
    app()

    # end of file