"""  aclu/ui/propsClasses/utils.py 
"""

from dataclasses import dataclass
from datetime import datetime as dt 
from typing import TypeVar, Dict
StrOrDict = TypeVar('StrOrDict', str, Dict) 


@dataclass
class Heading:
    level: int
    text: str
    unique: str = str(dt.timestamp(dt.now())) 

@dataclass
class Href:
    href: str 
    text: str
    unique: str = str(dt.timestamp(dt.now())) 


    ## end of file 