"""  aclu/ui/propsClasses/lists.py
"""

from dataclasses import dataclass
from typing import List  

from .utils import Heading, strOrDict  

@dataclass
class Unordered:
    heading: Heading 
    listItem: List[strOrDict] 


## end of file 