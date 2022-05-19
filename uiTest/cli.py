""" aclu/uiTest/cli.py 
"""

import typer 
from typing import Dict 

from . import app
from acluUtils import getModuleDir
import ui 
from ui.elements.lists import UnorderedList, OrderedList, DescriptionList, ListItem 
from ui.elements.utils import Heading, Title, Anchor  


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
def lists():
    """
    we have three types of lists to test, so let's make some coffee:
    unordered (ul) - stuff we need to make the coffee 
    ordered (ol) - steps to make the coffee 
    definition (dl) - some details regarding the supplies 
    """
    typer.echo('testing lists')
    starbucks = Anchor(href="https://www.starbucks.com/menu/at-home-coffee/via-instant", 
            contents="Starbucks Via instant coffee")
    suppliesHeading = Heading(2, "Coffee Making Supplies")
    suppliesList = UnorderedList([ListItem(starbucks),
        ListItem("knock-over resistant large coffee mug"),
        ListItem("Sugar"),
        ListItem("spoon to stir"),
        ListItem("Liquid level detector, plays 'Small World' when fluid reaches the probes."),
        ListItem("milk, real or oat, whatever is in the fridge")])
    suppliesList.attrValue('aria-labelledby', suppliesHeading.id())
    props = {
        'title': Title(contents='Lists Test'),
        'mainHeading': Heading(1, "Makin' Coffee, the Coffeenator"),
        'supplies': {
            'heading': suppliesHeading,
            'list': suppliesList
        }
    }
    showInBrowser(props, 'lists.html')



#######
@app.command()
def headings():
    typer.echo('testing heading generation')
    headingList = []
    for lvl in range(0, 8): 
        headingList.append(Heading(level=str(lvl), contents=f'Heading with Level: {lvl}'))
    headingList.append(Heading(level=1, contents=Anchor(href="https://blindgumption.com", contents="Blind Gumption", **{'class':'classValue', 'id':'uniqueId'})))
    headingList.append(Heading(className="someClass", level=2, contents="heading level 2 with someClass classname"))
    headingList.append(Heading(className="<someClass>", level=2, contents="heading level 2 with <someClass> classname"))
    headingList.append(Heading(uniqueId="somethingUnique", level=3, contents="heading level 3 with somethingUnique for unique"))
    headingList.append(Heading(uniqueId="'somethingUnique'", level=3, contents="heading level 3 with 'somethingUnique' for unique"))
    props ={
        'title': Title(contents='Headings Test'),
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