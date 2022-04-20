"""  aclu/ui/config.py
configuration of the jinja environment 
"""

import logging 
logger = logging.getLogger(__name__)

import os
import inspect 
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List 

env = None 

#######
def getDefaultTemplateDir() -> str:
    abspath = os.path.abspath(inspect.getabsfile(inspect.currentframe()))
    dirname, filename = os.path.split(abspath)
    return dirname + '/templates' 

#######
def initEnv(templateDirs: List[str] = None) -> Environment:
    """
    to override any of the templates in jinjable, 
    create a template with the same name,
    put it in some local directory,
    pass the local directory as an argument to initEnv 
    you can pass in multiple directories and jinja will search them in order for the given template 
    """
    # TODO: check the dirs are valid and don't modify passed in list  
    if templateDirs: templateDirs.append(getDefaultTemplateDir())
    else: templateDirs = getDefaultTemplateDir()
    global env 
    env = Environment(
        line_statement_prefix = '#',
        line_comment_prefix = '##',
        loader=FileSystemLoader(templateDirs),
        autoescape=select_autoescape()
    )
    return env 

## end of file