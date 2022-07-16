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

from ui.elements.tables  import Table


## end of file  