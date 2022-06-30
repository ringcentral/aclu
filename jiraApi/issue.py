""" aclu/jiraApi/issue.py 

An issue can be a simple issue in Jira,
or the base class of other Jira/Agile constructs, e.g. Epic 
It turns out instead of Epic extending Issue, Epic contains an Issue, that was cleaner 

the issue resource in Jira is part of the server platform API
Other resources can be considered special cases of an issue, e.g., epic 
the server platform API can be used to get such issues, but they might not have all the fields associated with the special use case
"""


import logging
logger = logging.getLogger(__name__)

import json 
from typing import Dict 

from . import jiraApiUtils
from .resourceBase import ResourceBase 

#######
class Issue(ResourceBase):
    """
    hardcoding query parameters for getting an Issue resource
    not a good practice, but expedient... TODO: use expand field from Jira issue resource 
    """
    details: str = 'expand=renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations'
    basic: str = 'fields= none'
    #####
    @classmethod
    def getIssue(cls, issueId: str, details: bool = False) -> object:
        if not details:
            url = f'{jiraApiUtils.platformUrl}/issue/{issueId}?{Issue.basic}'
        else:
            url = f'{jiraApiUtils.platformUrl}/issue/{issueId}?{Issue.details}'
        return super().get(url, f'issue/{issueId}')

    #####
    def __init__(self, issue: Dict):
        self.expand = issue.get('expand')
        self.id = issue.get('id')
        self.url = issue.get('self')
        self.key = issue.get('key')
        self.view = f'{jiraApiUtils.platformUrl}/preview/{self.key}'
        self.fields = issue.get('fields')        
        self.renderedFields = issue.get('renderedFields')
        self.names = issue.get('names')
        self.schema = issue.get('schema')
        self.operations = issue.get('operations')
        self.editmeta = issue.get('editmeta')
        self.changelog = issue.get('changelog')
        self.versionedRepresentations = issue.get('versionedRepresentations')
        self.raw = issue 

    #####
    def __repr__(self):
        if self.renderedFields and len(self.renderedFields) > 0:  # don't dump raw if Issue has details 
            return f'Id: {self.id}, key: {self.key}, view: {self.view}, url: {self.url}, number of rendered fields: {len(self.renderedFields)}'
        else:
            return json.dumps(self.raw, indent = 4)

    #####
    def getDetails(self) -> Dict:
        """
        if the GET for the issue resource included the expand query param,
        there should be several dicts detailing custom fields for the issue.
        This method goes through those dicts to create a single dict with all the useful information.
        """
        if not self.names:
            logger.info(f'No details for issue {self.key}')
            return None 
        else:
            pass 


## end of file 