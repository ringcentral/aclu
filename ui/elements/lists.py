"""  aclu/ui/elements/lists.py
Here we have elements specific to creating lists.
the list items (including <dt> and <dd>) are defined in here as well.
"""

from typing import List, Any

from .baseElements import BaseElement 
from .utils import Anchor, Heading, StrOrDict  

"""
<li>, <dt>, and <dd> are nearly the same element with different tags.
<dt> has more restrictions on its permitted content but I'm not sure this package needs to enforce that.
Maybe at some point I'll implement more types around content categories and build in more enforcement.
For now, I'm taking the C approach, so go ahead and corrupt memory.
Or in this case, implement nonsensical HTML documents.
"""

#######
class DesTerm(BaseElement):
    def __init__(self, contents: Any, ** kwArgs):
        super().__init__(tag='dt', contents=contents, **kwArgs)

#######
class DesDef(BaseElement):
    def __init__(self, contents: Any, ** kwArgs):
        super().__init__(tag='dd', contents=contents, **kwArgs)

#######
class DListItem:
    def __init__(self, terms: List[DesTerm], definition: DesDef):
        self.terms = terms
        self.definition = definition 

    def __repr__(self):
        entryString = ''
        for term in self.terms:
            entryString += f'{term}'
        entryString += f'{self.definition}'
        return entryString 

#######
class ListItem(BaseElement):
    def __init__(self, contents: Any, ** kwArgs):
        super().__init__(tag='li', contents=contents, **kwArgs)


####### 
class ListEntries(list):
    """
    this class only exists because __repr__ in BaseElement prints the square brackets 
    when it's generating the HTML for the list objects  
    """
    def __repr__(self):
        listString = ''
        for entry in self:
            listString += f'{entry}\n'
        return listString 


####### 
class BaseList(BaseElement):
    """
    <ol>, <ul>, and <menu> are syntactically the same thing (except for tag of course),
    And semantically they are aggregators of <li> elements with meaning fixed by the type of list.
    <dl> on the other hand, uses <dt> and <dd> elements which are more complicated
    The DListItem is an attempt to make list entries for <dl> look like those for the other lists.
    I didn't want to derive DListItem from BaseElement though as there's no tag, and it's not really an element.
    So in this BaseList class, I'm cheating, sort of, and letting the list of entries be Any 
    Since DListItem and ListItem only share object as a common ancestor  
    """
    def __init__(self, tag: str, entries: List[Any] = None, **kwArgs):
        self.entries = ListEntries()
        if entries:
            for entry in entries:
                self.entries.append(entry)
        super().__init__(tag=tag, contents=self.entries, **kwArgs)

    def addEntry(self, entry: Any) -> None: 
        self.entries.append(entry)

    def addEntries(self, entries: List[Any]) -> None:
        for entry in entries:
            self.entries.append(entry)

    def entryCount(self) -> int:
        return len(self.entries)


####### 
class UnorderedList(BaseList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('ul', entries, **kwArgs)


####### 
class OrderedList(BaseList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('ol', entries, **kwArgs)


####### 
class MenuList(BaseList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('menu', entries, **kwArgs)


####### 
class DescriptionList(BaseList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('dl', entries, **kwArgs)


## end of file 