##
# probably used mostly to create a list of epics on a given board
##

class Epic:
    def __init__(self, boardId, jiraCreds):
        self.boardId = boardId
        self.jiraCreds = jiraCreds 


## end of file 