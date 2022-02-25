##
# get as many detils for a given board as possible 
# details available depend on the type of board (scrum vs kanban)
# and we probably don't want all the issues, that could be too much.
##

import typer 
from .board import Board 


#######
def exploreBoard(brd) -> None:
    board = Board(brd)
    typer.echo(f"Exploring board, id: {board.id}, name: {board.name}, type: {board.type}")
    typer.echo('now get epics and sprints and try repr...')
    board.getEpics()
    board.getSprints()
    typer.echo(f'trying repr: {repr(board)}')



    ## end of file 