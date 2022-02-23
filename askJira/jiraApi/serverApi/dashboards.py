
import typer 
from typing import List, Optional, Tuple, Dict
from .. import apiUtils 
from . import app 
from . import jiraServerBaseUrl 


#######
def processDashboardResponse(resp: object, searchList: List[str] = None, caseSensitive: bool = False, printNames: bool = False, answerYes: bool = False) -> Tuple[str, List[Dict]]:
    next = None
    foundList = []
    dbo = apiUtils.getObjectFromJsonString(resp.text)
    if dbo != None:
        startAt = dbo['startAt']
        maxResults = dbo['maxResults']
        ## if too many items, total might not be calculated, thus not in the response  
        total = dbo.get('total', None) 
        typer.echo(f'started at: {startAt}, max results: {maxResults}, total available: {total}')
        if searchList or printNames:
            foundList = apiUtils.searchNamesInValues(dbo['dashboards'], searchList, caseSensitive, printNames)
        if answerYes or  typer.confirm('Continue to the next block of dashboards?'):
            ## can't use {} as next doesn't exist if on last page 
            next = dbo.get('next', None)
    ## this is not broken indentation, next was initiated to None 
    return next, foundList


#######
@app.command(name = 'dbs')
def dashboards(ctx: typer.Context, 
        searchList: Optional[List[str]] = typer.Option(None, "-s", "--search", help="use multiple -s options to search for multiple strings."),   
        caseSensitive: bool = typer.Option(False, "-c", "--caseSensitive", help="Flag to make search case sensitive, by default it is not."),
        printNames: bool = typer.Option(False, "-n", "--names", help="print the name of each dashboard."),
        pageSize: int = typer.Option(50, "-p", "--pageSize", help="how many dashboards to retrieve on each GET."),
        answerYes: bool = typer.Option(False, "-y", "--yes", help="don't ask to continue after each page, just do it!")
) -> None:
    """
    dbs is short for dashboards 
    must use either -s or -n, or both. 
    multiple -s options will result in finding dashboard with names containing any of those strings (OR'd) 
    use -c to make the search case sensitive
    if you use -y, you probably want a larger pageSize  
    if you use -n, you probably want a smaller pageSize  
    """
    if searchList: 
        typer.echo(f'Search dashboards for any of {searchList}')
        if caseSensitive:
            typer.echo('search is case sensitive')
        else:
            typer.echo('search is NOT case sensitive')
    elif printNames:
        typer.echo('print names of dashboards')
    else:
        typer.echo('either search or print, otherwise, why are you here?')
        return
    foundDashboards = apiUtils.getPaginatedResources(f'{jiraServerBaseUrl}dashboard', pageSize, searchList, caseSensitive,printNames, answerYes) 
    """
    resp = apiUtils.getResource(f'{jiraServerBaseUrl}dashboard?maxResults={pageSize}')
    while True:
        next, foundList = processDashboardResponse(resp, searchList, caseSensitive, printNames, answerYes)
        foundDashboards +=  foundList 
        if next != None:
            resp = apiUtils.getResource(next)
        else:
            break
    """
    ## we have found as many dashbords as we're going to,
    ## now what do we do with them?
    if searchList: 
        typer.echo(f'found {len(foundDashboards)} dashboards, now what?')


## end of file 