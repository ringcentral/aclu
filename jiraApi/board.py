"""
The Board class represents the main resource of the Agile API (Jira Software Server)

A board is used to aggregate issues, epics, sprints,
and a bunch of other resources. 
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Dict 
from .jiraApiUtils import StrOrDict 
from . import jiraApiUtils 
from .epic import Epic 
from .sprint import Sprint 

#######
class Board:
    @classmethod
    def getBoard(cls, brd: StrOrDict, jiraUrl: str) -> object:
        """
        """
        if isinstance(brd, str):
            """ we need to get the board dict first as this must be only an Id """
            id = brd  # for clarity and logging later 
            url = f'{jiraUrl}/board/{id}'
            resp, brd= jiraApiUtils.getResource(url, convertPayload=True)
            if brd is None:
                logger.info(f'could not find board with id: {id}')
        # now brd is either a dict as passed to getBoard
        # or a dict as returned by the get to the Jira API
        # note: brd could have been passed in as None or None returned by the get
        if brd: return cls(brd)
        else: return None 

    def __init__(self, brd: Dict, fullyPopulate: bool =False):
        """ 
        a Board is created with a Dict acquired from the Jira API
        Probably from previously searching across all boards on name matching given search strings,
        or we're here from getBoard.
        If all you have is a board id, you must use the class method getBoard
        And you can use getBoard with a dict from Jira as well for simplicity 
        """
        self.name = brd.get('name')
        self.type = brd.get('type')
        self.id = brd.get('id')
        self.url = brd.get('self') 
        """ 
        we have id, url, name, and type for the board.
        There's so much more we could get, how far do we go?
        epics, sprints, maybe even versions seem relevant
        leave those empty for now and let the user fill in what they want 
        """
        self.epics = []
        self.sprints = []

    #######
    def getEpics(self, includeIssues: bool = False) -> None:
        jiraEpics = jiraApiUtils.getPaginatedResources(f'{self.url}/epic')
        if len(jiraEpics) > 0:
            for ep in jiraEpics:
                self.epics.append(Epic(ep))
        else:
            logger.info(f'board {self.id}, {self.name} has no epics.  No epics for you!!')

    #######
    def getSprints(self, includeIssues: bool = False) -> None:
        jiraSprints = jiraApiUtils.getPaginatedResources(f'{self.url}/sprint')
        if len(jiraSprints) > 0:
            for spr in jiraSprints:
                self.sprints.append(Sprint(spr))
        else:
            logger.info(f'board {self.id}, {self.name} has no sprints.  No sprints for you!!')

    #######
    def __repr__(self):
        return f'Board id: {self.id}, name: {self.name}, type: {self.type} \n{self.epics} \n{self.sprints}'


## end of file 