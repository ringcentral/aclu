""" aclu/searchjira/cli.py 
"""

#from datetime import datetime as dt 
import typer
from typing import List, Dict, Any 

from . import app
from jiraApi import JiraApi, Issue, Board  
from acluUtils import printLongList, getModuleDir, storeLocals   
import ui 
from ui.elements.utils import Heading, Anchor, Paragraph, Title   
from ui.elements.lists import UnorderedList, ListItem 
# from ui.elements.tables import Caption 
from ui.builders.tableBuilder import TableInfo, RowInfo, createTableFromDicts  
import uiHelpers 

""" help strings that are used in multiple commands """ 
searchStringsHelp = "strings to search for in resource name, default is match any of the strings"
issueIdsHelp = "id, or key, of Jira issues.  Must match exactly, this is not a search, it is a GET operation"
idsHelp = "search strings are IDs of resources, much faster if you know what you're looking for"
containsAllHelp = "flag to indicate match all search words, default is to match any search word. "
caseSensitiveHelp = "flag to make search case sensitive"
showInBrowserHelp = "show search results in your default web browser"
detailsHelp = "include details of resources shown in the browser, only appplies if -b also set"


#######
def showInBrowser(props: Dict, template: str = 'listOfElements.html') -> None:
    """
    it is important to initialize the UI env from here to get the correct templates directory
    the templates directory in this package has templates specific to this package 
    do not be tempted to move showInBrowser to utils or the ui package
    this is why showinBrowser is two lines, once the initEnv is done,
    anything else can be done in the ui package 
    TODO: this will hopefully go away if/when I implement proper package resource management 
    """
    ui.initEnv([getModuleDir() + '/templates'])
    ui.openPage(props, template)

#######
def showElementsInBrowser(title: str, elements: List[Any]) -> None:
    props ={
        'title': Title(title),
        'elements': elements
    }
    typer.echo(f'opening new tab in your default browser for {title}')
    showInBrowser(props)


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
        dabrds = [jirapi.getDashboard(id) for id in searchstrings]
    else:
        dabrds = jirapi.findDashboards(searchstrings, containsall, casesensitive)
    if showinbrowser or printLongList(dabrds) == 'b':
        title = f"Searching for dashboards {', '.join(searchstrings)}"
        table = TableInfo(f'Found {len(dabrds)} dashboards', rowHeadingName='dashboard name, click to view in Jira')
        for db in dabrds:
            name = db.name if db.name else f'dashboard with id {db.id} does not exist'
            href = db.view
            row = RowInfo(heading=Anchor(href, name))
            table.addRow(row)
        elements =[]
        elements.append(Heading(1, title))
        elements.append(table.getTable())
        showElementsInBrowser(title, elements)

#######
@app.command()
def boards(ctx: typer.Context,
        searchstrings: List[str] = typer.Argument(..., help=searchStringsHelp),
        ids: bool = typer.Option(False, "-i", "--ids", help=idsHelp),
        containsall: bool = typer.Option(False, "-a", "--all", help=containsAllHelp),
        casesensitive: bool = typer.Option(False, "-c", "--casesensitive", help=caseSensitiveHelp),
        showinbrowser: bool = typer.Option(False, "-b", "--browser", help=showInBrowserHelp),
        details: bool = typer.Option(False, "-d", "--details", help=detailsHelp)
) -> None:
    jirapi = ctx.obj 
    searchstrings = list(set(searchstrings))
    brds: List[Board] = None 
    if ids:
        brds = [jirapi.getBoard(id) for id in searchstrings]
    else:
        brds = jirapi.findBoards(searchstrings, containsall, casesensitive)
    if showinbrowser or printLongList(brds) == 'b':
        title = f'Results from search boards for {", ".join(searchstrings)}'
        elements = [Heading(1, title)]
        for board in brds:
            if details: 
                board.getDetails(allIssues=True, backlog=True, epics=True)
            elements.append(uiHelpers.createHtmlForBoard(2, board))
        showElementsInBrowser(title, elements)


#######
@app.command()
def issues(ctx: typer.Context,
        issueids: List[str] = typer.Argument(..., help=issueIdsHelp),
        showinbrowser: bool = typer.Option(False, "-b", "--browser", help=showInBrowserHelp)
) -> None:
    jirapi: JiraApi = ctx.obj 
    issueids= list(set(issueids))
    issues: List[Issue] = [jirapi.getIssue(id, allFields=True) for id in issueids]
    if showinbrowser or printLongList(issues) == 'b':
        title = f'Issues from Ids: {", ".join(issueids)}'
        elements = [Heading(1, title)]
        for issue in issues:
            if issue.dne: # Does Not Exist  
                elements.append(Heading(2, f'no such issue with id {issue.id}'))
            else:
                elements.append(Heading(2, Anchor(issue.view, issue.key)))
                standardFields = issue.getAllFields(Issue.noCustomFields)
                standardFieldsTable = createTableFromDicts(f'Standard fields from {issue.key}', standardFields)
                elements.append(standardFieldsTable)
                customFields = issue.getAllFields(Issue.onlyCustomFields)
                customFieldsTable = createTableFromDicts(f'Custom fields from {issue.key}', customFields)
                elements.append(customFieldsTable)
                allFields = issue.getAllFields()
                allFieldsTable = createTableFromDicts(f'All fields from {issue.key}', allFields)
                elements.append(allFieldsTable)
        showElementsInBrowser(title, elements)


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