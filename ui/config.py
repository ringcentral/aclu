"""  aclu/ui/config.py
configuration of the jinja environment 
"""

import logging 
logger = logging.getLogger(__name__)

import os
import inspect 
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List 

from acluUtils import getModuleDir 

env = None 

#######
def getEnv():
    return env


#######
def getDefaultTemplateDir() -> str:
    return getModuleDir() + '/templates' 

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
    print(f'initEnv: templateDirs is {templateDirs}')
    global env 
    env = Environment(
        line_statement_prefix = '#',
        line_comment_prefix = '##',
        loader=FileSystemLoader(templateDirs),
        autoescape=select_autoescape()
    )
    return env 

## end of file