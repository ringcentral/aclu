"""  aclu/jiraApi/epic.py 
representing an epic resource from Jira 

Jira Epic resources are extensions of Jira Issue resources.
From that, I thought Epic should derive from Issue.
But a REST resource being an extension of another REST resource doesn't imply derivation in a clean OO sense.
The resources are different enough it made more sense to have the Epic contain an Issue and act 
more like a proxy to the underlying Issue resource. 
"""

import logging
logger = logging.getLogger(__name__)

from typing import Dict, List 

from . import jiraApiUtils
from .resourceBase import ResourceBase 
from .issue import Issue 

#######
class Epic(ResourceBase):

    #####
    @classmethod
    def getEpic(cls, epicId: str) -> object:
        url = f'{jiraApiUtils.agileUrl}/epic/{epicId}'
        return super().get(url, f'epic/{epicId}')

    #####
    def __init__(self, ep: Dict, getAllIssues: bool = False):
        self.id = ep.get('id')
        self.dne = ep.get('dne', False)
        self.name = ep.get('name')
        self.key = ep.get('key')
        self.view = f'{jiraApiUtils.baseUrl}/browse/{self.key}'
        self.summary = ep.get('summary')
        self.done = ep.get('done')
        self.url = ep.get('self')
        self.raw = ep 
        # do one query to learn how many issues are on this epic
        self.issuesList = []
        self.issuesCount = 0
        _, issues = jiraApiUtils.getResource(f'{self.url}/issue?maxResults=1', convertPayload=True)
        if issues:
            self.issuesCount = issues.get('total')
        else:
            logger.warning(f'failed to get list of issues for epic {self.id}, {self.key}')

    #####
    def getIssueDetails(self) -> List[Dict]:
        """
        In Jira, an epic is an issue with extra info
        it possibly has many custom fields which are stored in the associated Issue 
        """
        self.issue = Issue.getIssue(self.key)


    #####
    def __repr__(self):
        return (
            f'\n####### epic name: {self.name}, key: {self.key}, issue count: {self.issuesCount}, done: {self.done}'
            f'\nSummary: {self.summary}'
        )


## end of file