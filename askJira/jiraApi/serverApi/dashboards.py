"""
dashboards.py represents about the only thing interesting in the server platform API
  (other than issues of course but we get to those via the agile API) 
"""

import typer 
from typing import List, Optional, Tuple, Dict
from .. import apiUtils 
from . import app 
from . import jiraServerBaseUrl 


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
    ## what do we do with the dashboards?
    typer.echo(f'found {len(foundDashboards)} dashboards, now what?')


## end of file 