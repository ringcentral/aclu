"""  aclu/jiraApi/epic.py 
representing an epic resource from Jira 

Jira Epic resources are extensions of Jira Issue resources.
From that, I thought Epic should derive from Issue.
But a REST resource being an extension of another REST resource doesn't imply derivation in a clean OO sense.
The resources are different enough it made more sense to have the Epic contain an Issue and act 
more like a proxy to the underlying Issue resource. 
"""
from __future__ import annotations  ## support for forward type references, must be first line of code in file  

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
    def getEpic(cls, epicId: str, includeIssues: bool = False) -> Epic:
        url = f'{jiraApiUtils.agileUrl}/epic/{epicId}'
        epic: Epic  = super().get(url, f'epic/{epicId}')
        if includeIssues: epic.getIssues()
        return epic 

    #####
    def __init__(self, ep: Dict):
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
        self.containedIssues = []
        self.issuesCount = 0
        _, issues = jiraApiUtils.getResource(f'{self.url}/issue?maxResults=1', convertPayload=True)
        if issues:
            self.issuesCount = issues.get('total')
        else:
            logger.warning(f'failed to get list of issues for epic {self.id}, {self.key}')

    #####
    def getSelfIssue(self) -> None:
        """
        In Jira, an epic is an issue with extra info
        it possibly has many custom fields which are stored in the associated Issue 
        """
        self.selfIssue = Issue.getIssue(self.key)
        self.issueId = self.selfIssue.id
        self.issueKey = self.selfIssue.key 
        self.issueFields = self.selfIssue.fields 


    #####
    def __repr__(self):
        return (
            f'\n####### epic name: {self.name}, key: {self.key}, issue count: {self.issuesCount}, done: {self.done}'
            f'\nSummary: {self.summary}'
        )

    ##### 
    def getIssues(self) -> None:
        """
        get all the issues in this epic 
        nothing is returned but the containedIssues list should have Issues after getIssues completes 
        """
        issues = jiraApiUtils.getPaginatedResources(f'{self.url}/issue', fields=Issue.basicFields)
        if len(issues) > 0:
            self.containedIssues = [Issue(issue) for issue in issues]
        else:
            logger.info(f'Epic {self.id}, {self.key} has no issues')


## end of file