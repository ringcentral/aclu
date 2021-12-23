##
# get as many detils for a given board as possible 
# details available depend on the type of board (scrum vs kanban)
# and we probably don't want all the issues, that could be too much.
##

import typer 


#######
def exploreBoard(board: object, jiraCreds: tuple) -> None:
    typer.echo(f'Exploring board: {board["name"]}, type: {board["type"]}, id: {board["id"]}')



    ## end of file 