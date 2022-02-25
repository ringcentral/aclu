"""
boards.py is the main command in the agile command.
A board is the main aggregator of information for the Atlassian API.
It holds all the Epics and Sprints and other resources.
It is the main entry point for the CLU for the agile queries. 
"""

import typer 
from typing import List, Optional, Tuple, Dict
from .. import apiUtils 
from . import app 
from . import jiraAgileBaseUrl 
from .exploreBoard import exploreBoard 


#######
def printBoardTypes(boards: List[Dict]) -> None: 
    typeCounts = {'noValue': 0}
    for board in boards:
        brdType = board.get('type', None)
        if brdType != None:
            if typeCounts.get(brdType, None) != None:
                typeCounts[brdType] += 1
            else:
                typeCounts[brdType] = 1
        else:  ## there was no type property 
            typeCounts['noValue'] += 1 
    ## typeCounts is complete, now print it 
    typer.echo(f'There are {len(boards)} boards total and  {len(typeCounts.keys()) - 1} different types of boards')
    for k,v in typeCounts.items():
        typer.echo(f'{v} boards have type {k}')


#######
@app.command()
def boards(ctx: typer.Context, 
        boardId: Optional[str] = typer.Option(None, "-b", "--boardId", help="If you already know the Id of the board you want to examine, enter it on the command line."),   
        searchList: Optional[List[str]] = typer.Option(None, "-s", "--search", help="use multiple -s options to search for multiple strings."),   
        caseSensitive: bool = typer.Option(False, "-c", "--caseSensitive", help="Flag to make search case sensitive, by default it is not."),
        printNames: bool = typer.Option(False, "-n", "--names", help="print the name of each board."),
        countTypes: bool = typer.Option(False, "-t", "--types", help="count and print different types of boards, implies -y is also set."),
        pageSize: int = typer.Option(50, "-p", "--pageSize", help="how many boards to retrieve on each GET."),
        answerYes: bool = typer.Option(False, "-y", "--yes", help="don't ask to continue after each page, just do it!")
) -> None:
    """
    must use either -s or -n, or both, or -t if you just want a count of types of boards. 
    multiple -s options will result in finding board with names containing any of those strings (OR'd) 
    use -c to make the search case sensitive
    if you use -y, you probably want a larger pageSize  
    if you use -n, you probably want a smaller pageSize  
    """
    if boardId:
        ## hacking this up front so I can quickly look at a board 
        exploreBoard(boardId)
        return 
    if countTypes:
        answerYes = True 
        typer.echo('print the different types of boards and how many of each')
    else:
        if searchList or printNames: 
            typer.echo(f'Search boards for any of {searchList}')
            if caseSensitive:
                typer.echo('search is case sensitive')
            else:
                typer.echo('search is NOT case sensitive')
        else:
            typer.echo('either search, print, or count types, otherwise, why are you here?')
            return
    foundBoards = apiUtils.getPaginatedResources(f'{jiraAgileBaseUrl}board', pageSize, searchList, caseSensitive, printNames,answerYes)
    ## what do we do with the boards?
    if len(foundBoards) > 0:
        if countTypes:
            printBoardTypes(foundBoards)
        elif typer.confirm(f'found {len(foundBoards)}, want to go deeper?'):
            ## list the boards and ask for which one to dig in to
            choices = [f'{b["name"]}, {b["type"]}, id {b["id"]}' for b in foundBoards]
            option = apiUtils.getOption(choices)
            brd = foundBoards[option]
            exploreBoard(brd)
    elif searchList: 
        typer.echo(f'No boards found for search {searchList}')


## end of file 