"""
The Board class represents the main resource of the Agile API (Jira Software Server)

A board is used to aggregate issues, epics, sprints,
and a bunch of other resources. 
"""

import logging 
logger = logging.getLogger(__name__)

from .. import apiUtils 

#######
class Board:
    def __init__(self, baseUrl, id, name = None, type = None, fullyPopulate=False):
        """ 
        the board object can be created with only a base URL and id,
        in which case, the constructor queries to get the other board info.
        Or the board can be created after gettting all the board resource info from Jira and that info passed in here.
        """
        url = f'{baseUrl}/board/{id}/'
        self.id = id
        self.url = url 
        if name == None or type == None:
            ## we need to get the info from the API 
            resp, boardObj = apiUtils.getResource(url, convertPayload=True)
            if resp != None and boardObj != None:
                name = boardObj.get('name', None)
                type = boardObj.get('type', None)
            else:
                logger.warn(f'error getting board with id: {id}')
        self.name = name
        self.type = type 
        """ 
        we have id, url, name, and type for the board.
        There's so much more we could get, how far do we go?
        epics, sprints, maybe even versions seem relevant
        """


## end of file 