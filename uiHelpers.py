"""  aclu/uiHelpers.py

This set of functions is an attempt to vridge the jiraApi and ui packages.
I didn't want to have the jiraApi package depend on the ui package thus didn't want to include 
any of this functionality in something like, for example, jiraApi/board.py 

The right solution is probably to have  jiraApi and ui as packages 
both installable via pip (or choose your package manager), with much better names of course.
Then JiraApi could have the ui package on its dependency list and provide the 
functionality in this file as part of the classes for the jira resources.
Until then, it's all going into uiHelpers.py  
"""

import logging 
logger = logging.getLogger(__name__)

from typing import Any, Dict, List

from jiraApi.board import Board
from jiraApi.epic import Epic 
from jiraApi.issue import Issue 

from ui.builders.tableBuilder import RowInfo, TableInfo
from ui.elements.lists import ListItem, UnorderedList 
from ui.elements.tables  import Caption, Table
from ui.elements.utils import Anchor, Div, Heading, Span 


#######
def createListForAttributeValuesCounts(metaData: Dict) -> UnorderedList:
    """
    """
    attributeValuesCounts = UnorderedList()
    # attributeValuesCounts.attrValue('aria-label', 'counts for values for issues attributes')
    for attribute, valuesCounts in metaData.items():
        # use Span for this ListItem to use same text in aria-labelledby in sublist 
        liSpan = Span(f'counts for values for attribute {attribute}') 
        attributeValuesCounts.addElement(ListItem(liSpan))
        # create sublist that will be li for the attribute 
        countsList = UnorderedList()    
        # countsList.attrValue('aria-labelledby', liSpan.id())
        for val, count in valuesCounts.items():
            countsList.addElement(ListItem(f'\"{val}\" appears {count} times'))
        attributeValuesCounts.addElement(countsList)
    return attributeValuesCounts 


#######
def colnames(nWeeks: int) -> Dict[str,str]:
    if nWeeks < 3: raise ValueError(f'nWeeks must be at least 3, you passed in {nWeeks}')
    columnNames = {'0':'this week', '1':'last week'}
    columnNames.update({f'{w}':f'{w} weeks ago' for w in range(2,nWeeks - 1)})
    columnNames.update({f'{nWeeks - 1}':f'more than {nWeeks - 2} weeks ago'})
    return columnNames


#######
def createTableForCreatedUpdatedHistory(cuHistory: Dict) -> Table:
    """
    """
    # create column headings specifically based on number of weeks 
    nWeeks = len(cuHistory.get('created'))
    columnNames = colnames(nWeeks)
    cuhTableInfo = TableInfo('Counts of issues created and updated', 'activity', columnNames)
    for activity, history in cuHistory.items():
        ri = RowInfo(f'Issues {activity}')
        rd = {str(idx): history[idx] for idx in range(nWeeks)}
        ri.addEntries(**rd)
        cuhTableInfo.addRow(ri)
    return cuhTableInfo.getTable()


#######
def createTableForIssues(issues: List[Issue]) -> Table:
    ti:TableInfo = TableInfo('All Issues in the List', 'key')
    for issue in issues:
        ti.addRow(RowInfo(Anchor(issue.view, issue.key), issue.getFields()))
    return ti.getTable()


#######
def createHtmlForIssues(level: int, description: str, issues: List[Issue], includeIssuesTable: bool = False) -> Div:
    """
    level is used for any headings created as part of the returned HTML.
    description is needed to create captions and headings for the tables created here.
    issues is the list of Issue objects, see below for where they might come from.
    includeIssuesTable is to let the caller decide if the HTML should include a table with a row for each issue.

    There are many ways to get a list of Issues:
    - backlog from a board, 
    - all issues on a board, 
    - issues in an epic. 
    And it's all neatly wrapped up in a div.

    how to present the meta data?
    See the comments on method Issue.analyzeIssues for what's in the meta data.
    - For the values of each property, a list seems efficient
    - for the created and updated histories, a table should work well.

    Then the meta data will be followed by a table of the issues, if the caller says to (includeIssuesTable=True)
    """
    elements = [Heading(level, description)]
    metaData = Issue.analyzeIssues(issues)
    elements.append(Heading(level + 1, f'Counts for Different Values for Attributes for {description}'))
    elements.append(createListForAttributeValuesCounts(metaData.get('attributeValuesCounts')))
    elements.append(Heading(level + 1, f'History of activities for {description}'))
    elements.append(createTableForCreatedUpdatedHistory(metaData.get('cuHistory')))
    if includeIssuesTable:
        elements.append(Heading(level + 1, f'Table of all issues  for {description}'))
        elements.append(createTableForIssues(issues))
    return Div(elements)


#######
def createHtmlForEpic(level: int, epic: Epic) -> Div:
    """
    Level is needed for any headers created here.
    an Epic will have a list with properties of the list, 
    then a table showing all issues in that epic.
    Thus it's wrapped in a div.
    """
    pass 


#######
def createHtmlForBoard(level: int, board: Board) -> Div:
    """
    Level is needed for any headers created here.
    A Board should have a list of Epics and a backlog (a list of issues)
    It might also have a list of all issues on the board.
    In here we create some HTML with high level info for the board, 
    then HTML for each epic and for the backlog.
    And it's wrapped up nicely in a lovely div. 
    """
    pass 


## end of file  