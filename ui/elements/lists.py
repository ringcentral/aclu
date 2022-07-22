"""  aclu/ui/elements/lists.py
Here we have elements specific to creating lists.
the list items (including <dt> and <dd>) are defined in here as well.
"""

from typing import List, Any

from .baseElements import BaseElement, BaseElementList 
from .utils import Anchor, Heading

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
class UnorderedList(BaseElementList):
    def __init__(self, entries: List[ListItem] = None, **kwArgs):
        """
        technically a <ul> can have more than just <li> elements.
        For now though, it will be limited to ListItems.
        """
        super().__init__('ul', entries, **kwArgs)


####### 
class OrderedList(BaseElementList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('ol', entries, **kwArgs)


####### 
class MenuList(BaseElementList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('menu', entries, **kwArgs)


####### 
class DescriptionList(BaseElementList):
    def __init__(self, entries: List[Any] = None, **kwArgs):
        super().__init__('dl', entries, **kwArgs)


## end of file 