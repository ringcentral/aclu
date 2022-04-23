"""  aclu/ui/openpage.py
"""

import logging 
logger = logging.getLogger(__name__)

from datetime import datetime as dt 
from typing import Dict 
import webbrowser as wb 

from .config import getEnv 

#######
def  openPage(props: Dict, template: str) -> None:
    try:
        tmpl = getEnv().get_template(template)
        rendered = tmpl.render(props=props)
        thf = f'tmp_html_{dt.timestamp(dt.now())}.html'
        with open(thf, 'w') as f:
            f.write(rendered)
        wb.open(thf)
    except Exception as exc:
        logger.exception(f'Failed to open page for template {template}')


## end of file 