##
# boards.py started as a copy of serverApi\dashboards.py
# I moved some code into apiUtils but the server dashboards API 
# and agile boards API have some differences and duplicating code 
# seemed as unpleasant as hackery to try and break out response handling into a util
# specifically, the next string in dashboards vs the islast bool in boards
## 

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
    typer.echo(f'There are {len(typeCounts.keys()) - 1} different types of boards')
    for k,v in typeCounts.items():
        typer.echo(f'{v} boards have type {k}')


#######
def processBoardResponse(resp: object, searchList: List[str] = None, caseSensitive: bool = False, printNames: bool = False, answerYes: bool = False) -> Tuple[str, List[Dict]]:
    next = None
    foundList = []
    bo = apiUtils.getObjectFromJsonString(resp.text)
    if bo != None:
        startAt = bo['startAt']
        maxResults = bo['maxResults']
        ## if too many items, total might not be calculated, thus not in the response  
        total = bo.get('total', None) 
        typer.echo(f'started at: {startAt}, max results: {maxResults}, total available: {total}')
        if searchList or printNames:
            foundList = apiUtils.searchNamesInValues(bo['values'], searchList, caseSensitive, printNames)
        else:
            ## getting the list for processing later 
            foundList = bo['values']
        if answerYes or  typer.confirm('Continue to the next block of boards?'):
            ## have to manually construct 'next' unlike server/dashboards 
            if not bo['isLast']:
                next = f'{jiraAgileBaseUrl}board?maxResults={maxResults}&startAt={startAt + maxResults}'
    ## this is not broken indentation, next was initiated to None 
    return next, foundList


#######
@app.command()
def boards(ctx: typer.Context, 
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
    """
    resp, _ = apiUtils.getResource(f'{jiraAgileBaseUrl}board?maxResults={pageSize}')
    while True:  ## hacking a do while loop 
        next, foundList = processBoardResponse(resp, searchList, caseSensitive, printNames, answerYes)
        foundBoards +=  foundList 
        if next != None:
            resp, _ = apiUtils.getResource(next)
        else:
            break
    """
    ## we have found as many bords as we're going to,
    ## now what do we do with them?
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