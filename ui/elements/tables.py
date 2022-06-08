"""  aclu/ui/elements/tables.py
it's all about HTML tables in here
And HTML tables are ONLY for presenting tabular data.
If you use any of these table related elements to format the layout of your document,
you should be hunted down and ... well, something unpleasant ought to happen to you 
considering the audible pain you've inflicted on screen reader users 
it's 2022, use  CSS for layout and formatting  
"""

from typing import List, Any

from .baseElements import BaseElement, BaseElementList  
from .utils import Anchor, Heading, StrOrDict  


#######
class TableData(BaseElement):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__('td', contents, **kwArgs)


#######
class TableHeader(BaseElement):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__('th', contents, **kwArgs)


#######
class TableColumnHeader(TableHeader):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__(contents, scope='col', **kwArgs)


#######
class TableRowHeader(TableHeader):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__(contents, scope='row', **kwArgs)


#######
class TableRow(BaseElementList):
    def __init__(self, cells: List[Any] = None, **kwArgs):
        """
        cells should be a list of th or td elements 
        """
        super().__init__('tr', cells, **kwArgs)


"""
classes TableHead, TableBody, and TableFoot differ in only the four letters after the 't' for the tag string
hopefully there are no cut'n'paste errors here...
"""
#######
class TableHead(BaseElementList):
    def __init__(self, rows: List[Any] = None, **kwArgs):
        """
        rows should be a list of tr elements 
        """
        super().__init__('thead', rows, **kwArgs)


#######
class TableBody(BaseElementList):
    def __init__(self, rows: List[Any] = None, **kwArgs):
        """
        rows should be a list of tr elements 
        """
        super().__init__('tbody', rows, **kwArgs)


#######
class TableFoot(BaseElementList):
    def __init__(self, rows: List[Any] = None, **kwArgs):
        """
        rows should be a list of tr elements 
        """
        super().__init__('tfoot', rows, **kwArgs)


#######
class Caption(BaseElement):
    def __init__(self, contents: Any, **kwArgs):
        if not contents:
            raise ValueError("a Caption must have some contents")
        super().__init__('caption', contents, **kwArgs)


#######
class Table(BaseElementList):
    def __init__(self, caption: Caption, elements: List[Any] = None, **kwArgs):
        """
        a caption is not required in a table, here's where I start to get opinionated.
        And this opinion is toward accessibility.
        Tables with captions are nice when using single letter navigation.
        If I type 't' to go to the next table, I generally have to arrow up to understand what is in the table.
        A caption howerver will be read to me after typing 't' and landing on the next table.
        """
        if not caption: 
            raise ValueError("WTF, gives us a real caption my precious")
        self.caption = caption
        super().__init__('table', elements, **kwArgs)

    def __repr__(self):
        """
        to make caption a required element, I had to call it out  explicitly in the Table class.
        This keeps it from being part of the elements list in the base class.
        And that keeps it from being rendered in __repr__ of the base class.
        Table temporarily adds caption to the front of elements then pops it off after rendering
        It needs to be temporary in case the table is rendered multiple times
        """
        self.addElement(self.caption, front=True)
        repr = super().__repr__()
        self.elements.pop(0)
        return repr 
        self.addElement(self.caption, front=True)


## end of file 