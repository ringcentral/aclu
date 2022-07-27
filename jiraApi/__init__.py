""" aclu/jiraApi/__init__.py 
package for abstraction to the Jira API
I should move the class definition to its own file... someday 
"""

import logging 
logger = logging.getLogger(__name__)

import os 
from typing import List, Dict  

from . import jiraApiUtils 
from .board import Board 
from .dashboard import Dashboard 
from .epic import Epic 
from .issue import Issue 


#######
class JiraApi:
    user: str = None
    password: str = None 
    baseUrl:str = None 
    platformUrl: str = None
    agileUrl: str = None 
    def __init__(self, user: str = None, password: str = None, baseUrl: str = None):
        JiraApi.user = user if user else os.getenv('JIRA_USER')
        JiraApi.password = password if password else os.getenv('JIRA_PW')
        if self.user is None or self.password is None :
            raise ValueError('JiraApi must have a user and password') 
        jiraApiUtils.setJiraCreds((self.user, self.password))
        JiraApi.baseUrl = baseUrl if baseUrl else os.getenv('JIRA_BASE_URL')
        JiraApi.platformUrl = jiraApiUtils.buildUrl(self.baseUrl, 'rest/api/latest')
        JiraApi.agileUrl = jiraApiUtils.buildUrl(self.baseUrl, 'rest/agile/latest')
        if self.platformUrl is None or self.agileUrl is None:
            raise ValueError(f'baseUrl must have ben invalid, value is {self.baseUrl}')
        jiraApiUtils.setApiUrls(self.baseUrl, self.platformUrl, self.agileUrl)
        logger.info(f"user is {self.user}, baseUrl is {self.baseUrl}")

    def __repr__(self):
        return f"user is {self.user}, platformUrl is {self.platformUrl}, agileUrl is {self.agileUrl}"

    def findDashboards(self, searchList: List[str] = None, containsAll: bool = False, caseSensitive: bool = False, maxResults: int = 0, pageSize: int = 500) -> List[Dashboard]:
        searchList = list(set(searchList))
        tbrds = jiraApiUtils.getPaginatedResources(f'{self.platformUrl}/dashboard', searchList, containsAll, caseSensitive, maxResults, pageSize)
        return [Dashboard(brd) for brd in tbrds]

    def getDashboard(self, dashboardId: str) -> Dashboard:
        return Dashboard.getDashboard(dashboardId)

    def getBoardTypeCounts(self) -> Dict:
        """
        return a dict with keys as the strings that are type names 
        and values is the count of how many boards are of that type
        """
        allbrds = jiraApiUtils.getPaginatedResources(f'{self.agileUrl}/board')
        typeCounts = {'totalBoards': len(allbrds), 'noValue': 0}
        for board in allbrds:
            brdType = board.get('type', 'noValue')
            if typeCounts.get(brdType): typeCounts[brdType] += 1
            else: typeCounts[brdType] = 1
        return typeCounts 


    def findBoards(self, searchList: List[str] = None, containsAll: bool = False, caseSensitive: bool = False, maxResults: int = 0, pageSize: int = 500) -> List[Board]:
        searchList = list(set(searchList))
        tbrds = jiraApiUtils.getPaginatedResources(f'{self.agileUrl}/board', searchList, containsAll, caseSensitive, maxResults, pageSize)
        return [Board(brd) for brd in tbrds]

    def getBoard(self, boardId: str) -> Board:
        return Board.getBoard(boardId)


    def getEpic(self, epicId: str) -> Epic:
        return Epic.getEpic(epicId)

    def getIssue(self, issueId: str, allFields: bool = False) -> Issue:
        return Issue.getIssue(issueId, allFields)


## end of file 