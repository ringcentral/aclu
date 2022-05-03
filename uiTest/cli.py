""" aclu/uiTest/cli.py 
"""

import typer 
from typing import Dict 

from . import app
from acluUtils import getModuleDir
import ui 
from ui.propsClasses.utils import Heading 


#######
def showInBrowser(props: Dict, template: str) -> None:
    """
    it is important to initialize the UI env from here to get the correct templates directory
    the templates directory in this package has templates specific to this package 
    do not be tempted to move showInBrowser to utils or the ui package
    this is why showinBrowser is two lines, once the initEnv is done,
    anything else can be done in the ui package 
    this will hopefully go away if/when I implement proper package resource management 
    """
    ui.initEnv([getModuleDir() + '/templates'])
    ui.openPage(props, template)


#######
@app.command()
def headings():
    typer.echo('testing heading generation')
    headingList = []
    for lvl in range(0, 8): 
        headingList.append(Heading(level=str(lvl), text=f'Heading with Level: {lvl}'))
    headingList.append(Heading(className="someClass", level=2, text="heading level 2 with someClass classname"))
    headingList.append(Heading(className="<someClass>", level=2, text="heading level 2 with <someClass> classname"))
    headingList.append(Heading(uniqueId="somethingUnique", level=3, text="heading level 3 with somethingUnique for unique"))
    headingList.append(Heading(uniqueId="'somethingUnique'", level=3, text="heading level 3 with 'somethingUnique' for unique"))
    props ={
        'title': 'Headings Test',
        'headings': headingList
    }
    showInBrowser(props, 'headings.html')


####### 
@app.callback(invoke_without_command=True)
def main(
        configfile: str = typer.Option(None, "-c", "--configfile"),
        templatedirs: str = typer.Option(None, "-t", "--templatedirs")
) -> None:
    if configfile:
        typer.echo(f'using config file: {configfile}')
    if templatedirs:
        typer.echo(f'using template directories: {templatedirs}')
    typer.echo("that's it for the ui testing, hope it went well, and there's a page to view in your browser.")


## end of file 