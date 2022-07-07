""" aclu/jiraApi/issue.py 

An issue can be a simple issue in Jira,
or a base resource of other Jira/Agile constructs, e.g. Epic 
It turns out instead of Epic extending Issue, Epic contains an Issue, that was cleaner 

the issue resource in Jira is part of the server platform API
Other resources can be considered special cases of an issue, e.g., epic 
the server platform API can be used to get such issues, but they might not have all the fields associated with the special use case

I struggled quite a bit with which fields to track directly in the issue, and how.
A GET with no query parms will return a fields property of a dict with all possible fields, most of which are custom fields.
If you include versionedRepresentation in the expand query parm, the fields property is "hidden", see:
https://docs.atlassian.com/software/jira/docs/api/REST/8.22.4/#issue-getIssue

If I used only the renderedFields property which you have to get with the expand query parm,
several fields were missing.
I assume this has something to do with the versionedRepresentation,
but I didn't dig any deeper.  I had already spent way too much time on this.

As it stands now, 2022-07-07, I'll stick to the fields and remove all the renderedFields code.

We still need the expand query parms to get the names for the fields.
The fields dict has the field id, and the field value.
The names dict has the mapping from the field id to a useful name. 
"""


import logging
logger = logging.getLogger(__name__)

import json 
from typing import Dict, List, Callable 

from . import jiraApiUtils
from .resourceBase import ResourceBase 

#######
class Issue(ResourceBase):
    expandQueryParm: str = 'expand=fields,names' 
    """ predefined filters for getFields  """
    allFields: Callable[[str], bool] = lambda k: True
    onlyCustomFields: Callable[[str], bool] = lambda k: isinstance(k, str) and  k.startswith('custom')
    noCustomFields: Callable[[str], bool] = lambda k: isinstance(k, str) and not k.startswith('custom')
    #####
    @classmethod
    def getIssue(cls, issueId: str) -> object:
        url = f'{jiraApiUtils.platformUrl}/issue/{issueId}?{Issue.expandQueryParm}'
        return super().get(url, f'issue/{issueId}')

    #####
    def __init__(self, issue: Dict):
        self.id = issue.get('id')
        self.dne = issue.get('dne', False)
        self.url = issue.get('self')
        self.key = issue.get('key')
        self.view = f'{jiraApiUtils.baseUrl}/browse/{self.key}'
        self.fields = issue.get('fields')        
        self.names = issue.get('names')
        self.raw = issue 

    #####
    def __repr__(self):
        if self.dne:
            return f'Id: {self.id} Does Not Exist'
        else:
            return f'Id: {self.id}, key: {self.key}, view: {self.view}, url: {self.url}, number of fields: {len(self.fields)}, number of names : {len(self.names)}'

    #####
    def getFields(self, filter: Callable[[str], bool] = allFields) -> List[Dict]:
        """
        filter is a callable accepting one string argument, returning a bool
        if filter(k) is tru, that field is added to the returned dict  

        filter is a way to exclude, or include only those fields with ids of a certain format
        I did this instead of two, more narrow methods 
        to get only custom fields and only non-custom fields 
        see the class variables for predefined filters to effectively have those two methods 

        fields contains the field id and the field value.
        names contains the field id and a useful name for the field.
        Use both to get useful labels and values for non empty fields 
        """
        ## fieldList = []
        if not self.fields:
            logger.info(f'No fields returned for issue {self.key}')
            return []
        else:
            return [{'name': self.names.get(k), 'value':str(v), 'field id': k} for k,v in self.fields.items() if v and filter(k)]
            """
            for k, v in self.fields.items():
                if v and filter(k):
                    fieldList.append({'name': self.names.get(k), 'value':str(v), 'field id': k})
        return fieldList 
            """


## end of file 