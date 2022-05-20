"""  aclu/ui/elements/tables.py
it's all about HTML tables in here
If you use any of these table related elements to format the layout of your document,
you will be hunted down and ... well, something unpleasant ought to happen to you 
considering the audible pain you've inflicted on screen reader users 
use  CSS for layout and formatting  
"""

from typing import List, Any

from .baseElements import BaseElement 
from .utils import Anchor, Heading, StrOrDict  


#######
class TableData(BaseElement):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__('td', contents, **kwArgs)


#######
class Table(BaseElement):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__('table', contents, **kwArgs)


## end of file 