"""  aclu/jiraApi/board.py
The Board class represents the main resource of the Agile API (Jira Software Server)

A board is used to aggregate issues, epics, sprints,
and other resources. 
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Dict 

from . import jiraApiUtils 
from .resourceBase import ResourceBase 
from .epic import Epic 
from .sprint import Sprint 
from .issue import Issue 

#######
class Board(ResourceBase):

    #####
    @classmethod
    def getBoard(cls, boardId: str) -> object:
        url = f'{jiraApiUtils.agileUrl}/board/{boardId}'
        return super().get(url, f'board/{boardId}')


    #####
    def __init__(self, brd: Dict, fullyPopulate: bool =False):
        """ 
        a Board is created with a Dict acquired from the Jira API
        Probably from previously searching across all boards on name matching given search strings,
        If all you have is a board id, you must use the class method getBoard
        """
        self.name = brd.get('name')
        self.type = brd.get('type')
        self.id = brd.get('id')
        self.dne = brd.get('dne', False)
        self.url = brd.get('self') 
        """ 
        we have id, url, name, and type for the board.
        There's so much more we could get, how far do we go?
        epics, sprints, maybe even versions seem relevant
        leave those empty for now and let the user fill in what they want 
        """
        self.backlog = []
        self.epics = []
        self.sprints = []

    #####
    def getBacklog(self) -> None:
        backlog = jiraApiUtils.getPaginatedResources(f'{self.url}/backlog', fields='description')
        if len(backlog) > 0:
            self.backlog = [Issue(issue) for issue in backlog]
        else:
            logger.info(f'board {self.id}, {self.name} has no backlog.  Can that really be true?')


    #####
    def getEpics(self, includeIssues: bool = False) -> None:
        jiraEpics = jiraApiUtils.getPaginatedResources(f'{self.url}/epic')
        if len(jiraEpics) > 0:
            self.epics = [Epic(ep) for ep in jiraEpics]
        else:
            logger.info(f'board {self.id}, {self.name} has no epics.  No epics for you!!')

    #####
    def getEpic(self, epicId: str) -> Epic:
        return Epic.getEpic(epicId)


    #####
    def getSprints(self, includeIssues: bool = False) -> None:
        jiraSprints = jiraApiUtils.getPaginatedResources(f'{self.url}/sprint')
        if len(jiraSprints) > 0:
            self.sprints = [Sprint(spr) for spr in jiraSprints]
        else:
            logger.info(f'board {self.id}, {self.name} has no sprints.  No sprints for you!!')

    #####
    def __repr__(self):
        epicsStr = f'\n{self.epics}' if len(self.epics) > 0 else '' 
        sprintsStr = f'\n{self.sprints}' if len(self.sprints) > 0 else ''
        return f'Board id: {self.id}, name: {self.name}, type: {self.type} {epicsStr} {sprintsStr}'


## end of file 