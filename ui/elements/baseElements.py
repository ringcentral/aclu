"""  aclu/ui/elements/baseElements.py
classes in here are meant to be used to build HTML elements
"""

from dataclasses import dataclass 
from datetime import datetime as dt 
from markupsafe import escape 


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

    Unfortunately, by the nature of dataclasses with default values, 
    default values must be givin to the fields in derived classes.
    Those values have been set in a way they will hopefully be caught in testing. 
    """
    tagName: str = None 
    className: str = None 
    uniqueId: str = None 

    def getTagName(self):
        return escape(self.tagName) 

    def getIdAttribute(self):
        id = escape(self.uniqueId) if self.uniqueId else f'{self.getTagName()}-{str(dt.timestamp(dt.now()))}'
        return f'id="{id}"'

    def getClassAttribute(self):
        return f'class="{escape(self.className)}"' if self.className else '' 


## end of file 