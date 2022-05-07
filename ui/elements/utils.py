"""  aclu/ui/elements/utils.py 
simple dataclasses for props used by templates in ui/templates/utils.html
I realize I'm duplicating the definition of StrOrDict here (see acluutils.py
I want to keep ui a self contained package and maybe break it out from aclu some day )
"""

from dataclasses import dataclass
from datetime import datetime as dt 
from markupsafe import escape 
from typing import TypeVar, Dict
StrOrDict = TypeVar('StrOrDict', str, Dict) 

from .baseElements import BaseElement 

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