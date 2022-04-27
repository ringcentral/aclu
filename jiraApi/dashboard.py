"""  aclu/jiraApi/dashboard.py 
The dashboard is part of the platform thus in theory ban be used by the various Atlassian products 
We're using it only for the Agile project management 
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Dict 

from .jiraApiUtils import StrOrDict 
from . import jiraApiUtils 

#######
class Dashboard:
    @classmethod
    def getDashboard(cls, dbrd: StrOrDict, jiraUrl: str) -> object:
        """
        """
        if isinstance(dbrd, str):
            """ we need to get the dashboard dict first as this must be only an Id """
            id = dbrd  # for clarity and logging later 
            url = f'{jiraUrl}/dashboard/{id}'
            resp, dbrd= jiraApiUtils.getResource(url, convertPayload=True)
            if dbrd is None:
                logger.info(f'could not find dashboard with id: {id}')
        # now dbrd is either a dict as passed to getDashboard
        # or a dict as returned by the get to the Jira API
        # note: brd could have been passed in as None or None returned by the get
        if dbrd: return cls(dbrd)
        else: return None 


    def __init__(self, dbrd: Dict, fullyPopulate: bool =False):
        """ 
        a Dashboard is created with a Dict acquired from the Jira API
        Probably from previously searching across all boards on name matching given search strings,
        or we're here from getDashboard.
        If all you have is a dashboard id, you must use the class method getDashboard
        And you can use getDashboard with a dict from Jira as well for simplicity 
        """
        self.name = dbrd.get('name')
        self.id = dbrd.get('id')
        self.url = dbrd.get('self') 
        self.view = dbrd.get('view') 
        self.raw = dbrd 

    #######
    def __repr__(self):
        return f'Dashboard id: {self.id}, name: {self.name}'

    def printRaw(self):
        jiraApiUtils.shallowPrintDict(self.raw)


## end of file 