"""
representing a sprint resource from Jira 
"""

import logging 
logger = logging.getLogger(__name__)

from .. import apiUtils 
from . import jiraAgileBaseUrl 

class Sprint:
    def __init__(self, spri, getAllIssues:bool = False): 
        """
        like in Board(), spri can be either an Id of a Jira sprint, or 
        a dict already GET'ed from Jira 
        """
        if isinstance(spri, str):  ## spri is a sprint Id 
            url = f'{jiraAgileBaseUrl}sprint/{spri}'
            _, spri = apiUtils.getResource(url, convertPayload = True)
        if spri == None: 
            logger.warning("cannot create sprint with None input")
            return 
        self.id = spri.get('id')
        self.name = spri.get('name')
        self.state = spri.get('state')
        self.startDate = spri.get('startDate')
        self.endDate = spri.get('endDate')
        self.activatedDate = spri.get('activatedDate')
        self.completeDate = spri.get('completeDate')
        self.originBoardId = spri.get('originBoardId') 
        self.url = spri.get('self') 
        ## do one query to learn how many issues are on this sprint 
        self.issuesList = []
        self.issuesCount = 0
        _, issues = apiUtils.getResource(f'{self.url}/issue?maxResults=1', convertPayload=True)
        if issues: 
            self.issuesCount = issues.get('total')
        else:
            logger.warning(f'failed to get list of issues for sprint {self.id}, {self.name}')

    #######
    def __repr__(self):
        return f'\n####### Sprint id: {self.id}, name: {self.name}, state: {self.state}, issue count: {self.issuesCount}'


## end of file 