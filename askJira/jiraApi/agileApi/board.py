"""
The Board class represents the main resource of the Agile API (Jira Software Server)

A board is used to aggregate issues, epics, sprints,
and a bunch of other resources. 
"""

import logging 
logger = logging.getLogger(__name__)

from .. import apiUtils
from . import jiraAgileBaseUrl 
from .epic import Epic 
from .sprint import Sprint 

#######
class Board:
    def __init__(self, brd, fullyPopulate=False):
        """ 
        A Board is created either with a board Id, acquired in many different ways,
        or a board dict already returned by the Jira API probably from searching.
        The brd parameter could be either thus the isinstance checking below.
        """
        if isinstance(brd, str): ## brd is a board Id 
            ## get the board from Jira then proceed as though brd were the object to begin with 
            url = f'{jiraAgileBaseUrl}board/{brd}'
            _, brd= apiUtils.getResource(url, convertPayload=True)
        if brd == None:
            logger.warning('cannot create Board with no board object')
            return 
        self.name = brd.get('name')
        self.type = brd.get('type')
        self.id = brd.get('id')
        self.url = brd.get('self') 
        """ 
        we have id, url, name, and type for the board.
        There's so much more we could get, how far do we go?
        epics, sprints, maybe even versions seem relevant
        """
        self.epics = []
        self.sprints = []

    #######
    def getEpics(self, includeIssues: bool = False) -> None:
        jiraEpics = apiUtils.getPaginatedResources(f'{self.url}/epic')
        if len(jiraEpics) > 0:
            for ep in jiraEpics:
                self.epics.append(Epic(ep))
        else:
            logger.info(f'board {self.id}, {self.name} has no epics.  No epics for you!!')

    #######
    def getSprints(self, includeIssues: bool = False) -> None:
        jiraSprints = apiUtils.getPaginatedResources(f'{self.url}/sprint')
        if len(jiraSprints) > 0:
            for spr in jiraSprints:
                self.sprints.append(Sprint(spr))
        else:
            logger.info(f'board {self.id}, {self.name} has no sprints.  No sprints for you!!')

    #######
    def __repr__(self):
        return f'Board id: {self.id}, name: {self.name}, type: {self.type} \n {self.epics} \n {self.sprints}'


## end of file 