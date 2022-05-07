"""  aclu/ui/elements/lists.py
"""

from dataclasses import dataclass
from typing import List  

from .baseElements import BaseElement 
from .utils import Heading, StrOrDict  


####### 
@dataclass
class BaseList(BaseElement):
    heading: Heading = None 
    listItem: List[StrOrDict] = None 

####### 
@dataclass
class UnorderedList(BaseList):
    tagName: str = "ul"

####### 
@dataclass
class OrderedList(BaseList):
    tagName: str = "ol"

####### 
@dataclass
class DescriptionList(BaseList):
    tagName: str = "dl"


## end of file 