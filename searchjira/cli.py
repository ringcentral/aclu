""" aclu/searchjira/cli.py 
"""

#from datetime import datetime as dt 
import typer
from typing import List, Dict 

from . import app
from jiraApi import JiraApi, Issue  
from acluUtils import printLongList, getModuleDir, storeLocals   
import ui 
from ui.elements.utils import Heading, Anchor, Paragraph   
from ui.elements.tables import Caption 
from ui.builders.tableBuilder import TableInfo, RowInfo, createTableFromDicts  


""" help strings that are used in multiple commands """ 
searchStringsHelp = "strings to search for in resource name, default is match any of the strings"
issueIdsHelp = "id, or key, of Jira issues.  Must match exactly, this is not a search, it is a GET operation"
detailsHelp = "True if you want details for requested resources"
idsHelp = "search strings are IDs of resources, much faster if you know what you're looking for"
containsAllHelp = "flag to indicate match all search words, default is to match any search word. "
caseSensitiveHelp = "flag to make search case sensitive"
showInBrowserHelp = "show search results in your default web browser"


#######
def showInBrowser(props: Dict, template: str) -> None:
    """
    it is important to initialize the UI env from here to get the correct templates directory
    the templates directory in this package has templates specific to this package 
    do not be tempted to move showInBrowser to utils or the ui package
    this is why showinBrowser is two lines, once the initEnv is done,
    anything else can be done in the ui package 
    this will hopefully go away if/when I implement proper package resource management 
    """
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
    locs = storeLocals('dashboards', locals())
    jirapi = ctx.obj 
    searchstrings = list(set(searchstrings))
    if ids:
        ## dabrds = [db if db else {id: "Does Not Exist"} for id in searchstrings if (db := jirapi.getDashboard(id)) or True]
        dabrds = [db for id in searchstrings if (db := jirapi.getDashboard(id)) or (db := {id: "Does Not Exist"} if not db else db)]
    else:
        dabrds = jirapi.findDashboards(searchstrings, containsall, casesensitive)
    if showinbrowser or printLongList(dabrds) == 'b':
        typer.echo('opening new tab in your default browser')
        table = TableInfo(Caption(f'Found {len(dabrds)} dashboards'), rowHeadingName='dashboard name, click to view in Jira')
        for db in dabrds:
            name = db.name
            href = db.view
            row = RowInfo(heading=Anchor(href, name))
            table.addRow(row)
        elements =[]
        elements.append(Heading(2, 'Search Properties'))
        elements.append(Paragraph(f'{locs}'))
        elements.append(table.getTable())
        props ={
            'title': ' '.join(searchstrings),
            'elements': elements
        }
        showInBrowser(props, 'listOfElements.html')
    ## if len(dabrds) > 0: dabrds[0].printRaw()


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


#######
@app.command()
def issues(ctx: typer.Context,
        issueids: List[str] = typer.Argument(..., help=issueIdsHelp),
        details: bool = typer.Option(False, "-d", "--details", help=detailsHelp),
        showinbrowser: bool = typer.Option(False, "-b", "--browser", help=showInBrowserHelp)
) -> None:
    jirapi = ctx.obj 
    issueids= list(set(issueids))
    args = [[issue, True]if details else [issue, False] for issue in issueids]
    issues = [issue for arg in args if (issue := jirapi.getIssue(*arg)) or (issue := {arg[0]: "Does Not Exist"} if not issue else issue)]
    if showinbrowser or printLongList(issues) == 'b':
        typer.echo('showing issues in new tab in your default browser')
        title = f'Issues from Ids: {", ".join(issueids)}'
        elements =[]
        elements.append(Heading(1, title))
        for issue in issues:
            if isinstance(issue, Issue):
                elements.append(Heading(2, Anchor(issue.view, issue.key)))
                if details:
                    standardFields = issue.getFields(Issue.noCustomFields)
                    standardFieldsTable = createTableFromDicts(f'rendered standard fields from {issue.key}', standardFields)
                    elements.append(standardFieldsTable)
                    customFields = issue.getFields(Issue.onlyCustomFields)
                    customFieldsTable = createTableFromDicts(f'rendered custom fields from {issue.key}', customFields)
                    elements.append(customFieldsTable)
                    allFields = issue.getFields()
                    allFieldsTable = createTableFromDicts(f'All rendered fields from {issue.key}', allFields)
                    elements.append(allFieldsTable)
            else: 
                # this should be the no issue found error dict 
                elements.append(Heading(2, str(issue)))
        props ={
            'title': title,
            'elements': elements
        }
        showInBrowser(props, 'listOfElements.html')


#######
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