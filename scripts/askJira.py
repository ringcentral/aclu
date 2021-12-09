#!/usr/bin/env python

import typer
import serverApi


app = typer.Typer()
app.add_typer(serverApi.app, name='server')

jiraServerBaseUrl = 'https://jira.ringcentral.com/rest/api/latest/'

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
    if ctx.invoked_subcommand == 'server':
        ctx.obj = (jira_user, jira_pw, jiraServerBaseUrl)


if __name__ == "__main__":
    app()

    # end of file
