"""
representing an epic resource from Jira 
"""

import logging
logger = logging.getLogger(__name__)

from . import jiraApiUtils

class Epic:
    def __init__(self, ep, jiraUrl: str = None, getAllIssues: bool = False):
        """
        like in Board(), ep can be either an Id of a Jira epic, or 
        a dict already GET'ed from Jira 
        """
        if isinstance(ep, str):  # ep is an epic Id
            url = f'{jiraUrl}/epic/{ep}'
            _, ep = jiraApiUtils.getResource(url, convertPayload=True)
        if ep == None:
            raise ValueError('invalid input to Epic')
        self.id = ep.get('id')
        self.name = ep.get('name')
        self.key = ep.get('key')
        self.summary = ep.get('summary')
        self.done = ep.get('done')
        self.url = ep.get('self')
        # do one query to learn how many issues are on this epic
        self.issuesList = []
        self.issuesCount = 0
        _, issues = jiraApiUtils.getResource(
            f'{self.url}/issue?maxResults=1', convertPayload=True)
        if issues:
            self.issuesCount = issues.get('total')
        else:
            logger.warning(f'failed to get list of issues for epic {self.id}, {self.key}')

    #######
    def __repr__(self):
        return (
            f'\n####### epic name: {self.name}, key: {self.key}, issue count: {self.issuesCount}, done: {self.done}'
            f'\nSummary: {self.summary}'
        )


# end of file
