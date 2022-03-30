"""
__init__.py in jiraApi 
package for abstraction to the Jira API
"""

import logging 
logger = logging.getLogger(__name__)

import os 
import validators 
from typing import Dict, List 
from .jiraApiUtils import StrOrDict
from . import jiraApiUtils 
from .board import Board 
from .dashboard import Dashboard 


#######
def buildUrl(base: str, endpoint: str) -> str:
    url = None 
    try:
        base = base.strip()
        endpoint = endpoint.strip()
        if validators.url(base) == True:
            # remove trailing slash from base 
            # and leading slash from endpoint, if either exists
            base = base if base[-1] != '/' else base[:-1]
            endpoint = endpoint if endpoint[0] != '/' else endpoint[1:]
            url = f'{base}/{endpoint}'
            # validate again in case endpoint had garbage 
            if validators.url(url) != True:
                url = None
    except Exception:
        pass 
    return url 


#######
class JiraApi:
    def __init__(self, user: str = None, password: str = None, baseUrl: str = None):
        self.user = user if user else os.getenv('JIRA_USER')
        self.password = password if password else os.getenv('JIRA_PW')
        if self.user is None or self.password is None :
            raise ValueError('JiraApi must have a user and password') 
        jiraApiUtils.setJiraCreds((self.user, self.password))
        self.baseUrl = baseUrl if baseUrl else os.getenv('JIRA_BASE_URL')
        self.platformUrl = buildUrl(self.baseUrl, 'rest/api/latest')
        self.agileUrl = buildUrl(self.baseUrl, 'rest/agile/latest')
        if self.platformUrl is None or self.agileUrl is None:
            raise ValueError(f'baseUrl must have ben invalid, value is {self.baseUrl}')
        logger.info(f"user is {self.user}, baseUrl is {self.baseUrl}")

    def __repr__(self):
        return f"user is {self.user}, platformUrl is {self.platformUrl}, agileUrl is {self.agileUrl}"

    def findDashboards(self, searchList: List[str] = None, caseSensitive: bool = False, maxResults: int = 0, pageSize: int = 500) -> List[Dict]:
        return jiraApiUtils.getPaginatedResources(f'{self.platformUrl}/dashboard', searchList, caseSensitive, maxResults, pageSize)

    def getDashboard(self, dbrd: StrOrDict) -> Dict:
        return Dashboard.getDashboard(dbrd, self.platformUrl)

    def findBoards(self, searchList: List[str] = None, caseSensitive: bool = False, maxResults: int = 0, pageSize: int = 500) -> List[Dict]:
        return jiraApiUtils.getPaginatedResources(f'{self.agileUrl}/board', searchList, caseSensitive, maxResults, pageSize)

    def getBoard(self, brd: StrOrDict) -> Dict:
        return Board.getBoard(brd, self.agileUrl)


## end of file 