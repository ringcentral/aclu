"""  aclu/jiraApi/dashboard.py 
The dashboard is part of the platform thus in theory can be used by the various Atlassian products 
We're using it only for the Agile project management 
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Dict 

from . import jiraApiUtils 
from .resourceBase import ResourceBase 

#######
class Dashboard(ResourceBase):
    @classmethod
    def getDashboard(cls, dbrdId: str, ) -> object:
        url = f'{jiraApiUtils.platformUrl}/dashboard/{dbrdId}'
        return super().get(url, f'dashboard/{dbrdId}')


    def __init__(self, dbrd: Dict, fullyPopulate: bool =False):
        """ 
        a Dashboard is created with a Dict acquired from the Jira API
        Probably from previously searching across all boards on name matching given search strings,
        or we're here from getDashboard.
        If all you have is a dashboard id, you must use the class method getDashboard
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