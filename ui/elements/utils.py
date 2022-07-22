"""  aclu/ui/elements/utils.py 
simple dataclasses for props used by templates in ui/templates/utils.html
I realize I'm duplicating the definition of StrOrDict here (see acluutils.py
I want to keep ui a self contained package and maybe break it out from aclu some day )
"""

from datetime import datetime as dt 
from markupsafe import escape 
from typing import Dict, Any, List

from .baseElements import BaseElement, BaseElementList  


####### 
class Anchor(BaseElement):
    def __init__(self, href: str, contents: Any, **kwArgs):
        self.href = str(escape(href))
        super().__init__(tag='a', contents=contents, href=self.href, **kwArgs)


####### 
class Div(BaseElementList):
    """
    a <div> is mainly a way to group elements thus it makes 
    sense for it to derive from BaseElementList.
    """
    def __init__(self, elements: List[Any], **kwArgs):
        super().__init__('div', elements, **kwArgs)


####### 
class Heading(BaseElement):
    def __init__(self, level: int, contents: Any, **kwArgs):
        self.level = level
        super().__init__(tag=f'h{level}', contents=contents, **kwArgs)


####### 
class Paragraph(BaseElement):
    """
    should the paragraph be a BaseList?  No.
    A <p> element generally wraps text though is often used to wrap other elements (I'd argue div with CSS should be used for that).
    it is perfectly legit though to have HTML elements wihtin text (e.g., <span> and <a>).
    Then how are those inline elements rendered?  
    Glad you asked.  f strings of course.
    For example:
    Paragraph(f'Visit, {Anchor("https://mysite.com", "My Lovely Website")}, to learn about me')
    will render the output:
    <p>Visit, <a href="https://mysite.com">My Lovely Website</a>, to learn about me</p>
    Objects of classes derived from Baseelement are rendered as HTML when evaluated by jinja in a template. 
    """
    def __init__(self, contents: Any, **kwArgs):
        super().__init__(tag='p', contents=contents, **kwArgs)


#######
class Span(BaseElement):
    def __init__(self, contents: Any, **kwArgs):
        super().__init__(tag='span', contents=contents, **kwArgs)


####### 
class Title(BaseElement):
    def __init__(self, contents: str, **kwArgs):
        if not isinstance(contents, str):
            raise TypeError("Title contents must be a string")
        self.titleStr = str(escape(contents))
        super().__init__(tag='title', contents=self.titleStr, **kwArgs)



## end of file 