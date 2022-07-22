""" aclu/jiraApi/issue.py 

An issue can be a simple issue in Jira,
or a base resource of other Jira/Agile constructs, e.g. Epic 
instead of Epic extending Issue, I made Epic contain an Issue, that was cleaner 

the issue resource in Jira is part of the server platform API
Other resources can be considered special cases of an issue, e.g., epic 
the server platform API can be used to get such issues, but they might not have all the fields associated with the special use case
thus, for example, use the agile API to get epic resources to get all the fields associated with an epic.

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
from __future__ import annotations  ## support for forward type references, must be first line of code in file  

import logging
logger = logging.getLogger(__name__)

from datetime import datetime as dt 
from dateutil.parser import parse 
from dateutil import tz 
import json 
from typing import Dict, List, Callable 

from . import jiraApiUtils
from .resourceBase import ResourceBase 

#######
class Issue(ResourceBase):
    basicFields= 'created,updated,lastViewed,priority,status,issuetype,summary'
    expandQueryParm: str = 'fields,names' 
    # the default list of attributes to be analyzed (summarize their different values)
    defaultAttributesToAnalyze: List[str] = ['status', 'priority', 'issueType']
    # predefined filters for getFields 
    allFields: Callable[[str], bool] = lambda k: True
    onlyCustomFields: Callable[[str], bool] = lambda k: isinstance(k, str) and  k.startswith('custom')
    noCustomFields: Callable[[str], bool] = lambda k: isinstance(k, str) and not k.startswith('custom')
    #####
    @classmethod
    def getIssue(cls, issueId: str, allFields: bool = False) -> Issue:
        if allFields:
            url = f'{jiraApiUtils.platformUrl}/issue/{issueId}?expand={Issue.expandQueryParms}'
        else:
            url = f'{jiraApiUtils.platformUrl}/issue/{issueId}?fields={Issue.basicFields}'
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
        # get all the basic fields 
        # created,updated,lastViewed,priority,status,issuetype,summary
        self.created = parse(self.fields.get('created'))
        self.updated = parse(self.fields.get('updated'))
        self.lastViewed = parse(self.fields.get('lastViewed')) if self.fields.get('lastViewed') else self.created 
        self.priority = self.fields.get('priority').get('name')
        self.status = self.fields.get('status').get('name')
        self.statusCategory = self.fields.get('status').get('statusCategory').get('name')
        self.issueType = self.fields.get('issuetype').get('name')
        self.summary = self.fields.get('summary') 

    #####
    def __repr__(self):
        if self.dne:
            return f'Id: {self.id} Does Not Exist'
        else:
            return f'Id: {self.id}, key: {self.key}, view: {self.view}, url: {self.url}, number of fields: {len(self.fields) if self.fields else 0}, number of names : {len(self.names) if self.names else 0}'

    #####
    def getFields(self) -> Dict:
        """
        get only the fields that are attributes of the issue object.
        use getAllFields if you want to iterate through the fields and names dicts
        this method is most likely used to generate a row in a HTML table 
        but it would be bad to let the UI details creep in to the jiraApi package... 
        """
        return {
            # 'key': self.key,
            # 'view': self.view,
            'summary': self.summary,
            'priority': self.priority,
            'status': self.status,
            ## 'status category': self.statusCategory,
            'issue type': self.issueType,
            'created': self.created.strftime('%Y-%m-%d %H:%M'),
            'updated': self.updated.strftime('%Y-%m-%d %H:%M')
        }

    #####
    def getAllFields(self, filter: Callable[[str], bool] = allFields) -> List[Dict]:
        """
        getAllFields iterates through the fields and names dicts, assuming they are  here.
        'All' is in contrast to getFields which returns very few fields.
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
        if not self.names:
            logger.info(f'No names for issue {self.key}.  you must use Issue.getIssue(allFields=True) to have fields and names')
            return []
        else:
            return [{'name': self.names.get(k), 'value':str(v), 'field id': k} for k,v in self.fields.items() if v and filter(k)]

    #####
    @staticmethod
    def analyzeIssues(issues: List[Issue], attributes: List[str] = defaultAttributesToAnalyze, weeksToLookBack: int = 7) -> Dict:
        """
        weeksToLookBack (must be at least 3) is used to calculate how many issues were created/updated in the last n weeks.
        for each attribute in the attributes list,
        we want to know the different values in the issues and how many times each value appears.
        The resulting dict has an entry with each attribute as a key 
        and its value is a dict with each value seen for that attribute as a key,
        and how many times that value occured as the value.

        We also want to know how many issues were created/updated within the last several weeks.
        """
        if weeksToLookBack < 3: raise ValueError('weeksToLookBack must be at least 3')
        attrValuesCounts = {attr:{} for attr in attributes}
        # in the history lists, the index is the number of weeks ago an issue was created or updated. 
        createdHistory = [0] * (weeksToLookBack + 1)
        updatedHistory = [0] * (weeksToLookBack + 1)
        nowDate = dt.now(tz=tz.tzutc()).date()
        for issue in issues:
            for attr in attributes:
                if (av := getattr(issue, attr, None)) != None:
                    # increment the count for the attr value in the appropriate dict of counts 
                    attrCounts = attrValuesCounts.get(attr)
                    if attrCounts.get(av, None) is None: attrCounts[av] = 1
                    else: attrCounts[av] += 1
                else:
                    logger.debug(f'{issue.key} has no attribute {attr}')
            ## now check created and updated times 
            createdWeeksAgo = (nowDate - issue.created.date()).days // 7  
            createdWeeksAgo = weeksToLookBack if createdWeeksAgo > weeksToLookBack else createdWeeksAgo 
            createdHistory[createdWeeksAgo] += 1
            updatedWeeksAgo = (nowDate - issue.updated.date()).days // 7  
            updatedWeeksAgo = weeksToLookBack if updatedWeeksAgo > weeksToLookBack else updatedWeeksAgo 
            updatedHistory[updatedWeeksAgo] += 1   
        return {'attributeValuesCounts': attrValuesCounts, 'cuHistory': {'created':createdHistory, 'updated': updatedHistory}}


## end of file 