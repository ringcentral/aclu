"""  aclu/ui/propsClasses/utils.py 
simple dataclasses for props used by templates in ui/templates/utils.html
I realize I'm duplicating the definition of StrOrDict here (see acluutils.py
I want to keep ui a self contained package and maybe break it out from aclu some day )
"""

from dataclasses import dataclass
from datetime import datetime as dt 
from typing import TypeVar, Dict
StrOrDict = TypeVar('StrOrDict', str, Dict) 


@dataclass
class BaseElement:
    """
    attributes applicable to all HTML elements are defined in the base class 
    Some MUST be overridden by the derived class (e.g., tagName)
    but having them here makes it easier to support getAttribute methods that might rely on other attributes 

    tagName really is required though has the default None here
    Each derived class will override the tagName based on the element being created by that class
    tagName is defined here so it can be used to generate a unique ID from a method in the base class 

    className, OTOH, really is optional thus getting the attribute returns '' if there is no className 

    Unfortunately, by the nature of datablasses with default values, 
    default values must be givin to the fields in derived classes.
    Those values have been set in a way they will hopefully be caught in testing. 
    """
    _tagName: str = None 
    _className: str = None 
    _unique: str = str(dt.timestamp(dt.now())) 

    def getTagName(self):
        return self._tagName 
    def getIdAttribute(self):
        return f'id="{self.getTagName()}-{self._unique}"'

    def getClassAttribute(self):
        return f'class="{self._className}"' if self._className else '' 


@dataclass
class Heading(BaseElement):
    level: int = 1
    text: str = "ERROR: This is the default text in Heading"

    def getTagName(self):
        return f'h{self.level}'

@dataclass
class Href(BaseElement):
    _tagName: str = "a"
    href: str = "https://blindgumption.com"
    text: str = "ERROR: you need to supply text for the anchor"


    ## end of file 