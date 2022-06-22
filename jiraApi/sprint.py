"""
representing a sprint resource from Jira 
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Dict 

from . import jiraApiUtils 

class Sprint:
    #####
    @classmethod
    def getSprint(cls, sprintId: str) -> object:
        url = f'{jiraApiUtils.agileUrl}/sprint/{sprintId}'
        return super().get(url, f'sprint/{sprintId}')

    def __init__(self, spri: Dict, getAllIssues: bool = False): 
        self.id = spri.get('id')
        self.name = spri.get('name')
        self.state = spri.get('state')
        self.startDate = spri.get('startDate')
        self.endDate = spri.get('endDate')
        self.activatedDate = spri.get('activatedDate')
        self.completeDate = spri.get('completeDate')
        self.originBoardId = spri.get('originBoardId') 
        self.url = spri.get('self') 
        self.raw = spri
        ## do one query to learn how many issues are on this sprint 
        self.issuesList = []
        self.issuesCount = 0
        _, issues = jiraApiUtils.getResource(f'{self.url}/issue?maxResults=1', convertPayload=True)
        if issues: 
            self.issuesCount = issues.get('total')
        else:
            logger.warning(f'failed to get list of issues for sprint {self.id}, {self.name}')

    #####
    def __repr__(self):
        return f'\n####### Sprint name: {self.name}, issue count: {self.issuesCount}, state: {self.state}'


## end of file 