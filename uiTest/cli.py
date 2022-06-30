""" aclu/uiTest/cli.py 
"""

import typer 
from typing import Dict 

from . import app
from acluUtils import getModuleDir
import ui 
from ui.elements.lists import UnorderedList, OrderedList, DescriptionList, ListItem, DListItem, DesTerm, DesDef  
from ui.elements.utils import Heading, Title, Anchor, Paragraph   
from ui.builders.tableBuilder import TableInfo, createTableFromDicts  
from uiTest.elementsMdn import getElementsTables, mdnAnchor 


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
def elements(outputfile:str = typer.Option("elementsData.html", "-o", "--outputfile")) -> None:
    """
    elements is used to test Table and the tableBuilder
    it will scrape HTML element reference info from MDN and present it in a table 
    """
    typer.echo(f'using output file: {outputfile}')
    elements = []
    (currentElementsTable, deprecatedElementsTable) = getElementsTables(outputfile)
    if not currentElementsTable or not deprecatedElementsTable:
        elements.append(Heading(1, 'failed to scrape elements from {mdnAnchor}'))
    else:
        elements.append(Heading(1,'Tables of HTML Elements '))
        elements.append(Paragraph(f'Information in the below tables was scraped from {mdnAnchor}.'))
        elements.append(Heading(2, 'Currently Supported HTML Elements'))
        elements.append(currentElementsTable.getTable())
        elements.append(Heading(2, 'Deprecated HTML Elements'))
        elements.append(deprecatedElementsTable.getTable())
    props ={
        'title': Title('HTML Elements Reference from MDN'),
        'elements': elements
    }
    showInBrowser(props, 'listOfElements.html')

#######
@app.command()
def ctfd(
        lower: int = typer.Option(1, "-l", "--lower"),
        upper: int = typer.Option(10, "-u", "--upper")
):
    """
    to test the createTableFromDicts function from tableBuilder 
    """
    rows = []
    for x in range(lower,upper + 1):
        row = {'base': x}
        row.update(dict([(y, x**y) for y in range(lower, upper + 1)]))
        rows.append(row)
    ## we have a matrix, now display it in an HTML table 
    table = createTableFromDicts('base number raised to column heading number', rows)
    elements = []
    elements.append(Heading(1,'Testing createTableFromDicts function in tableBuilder'))
    elements.append(Heading(2, 'Raise base to power (column heading number)'))
    elements.append(table)
    props ={
        'title': Title('Testing createTableFromDicts in tableBuilder'),
        'elements': elements
    }
    showInBrowser(props, 'listOfElements.html')



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
    suppliesList = UnorderedList([ListItem(f'coffee is from {starbucks}'),
            ListItem("knock-over resistant large coffee mug"),
            ListItem("Sugar"),
            ListItem("spoon to stir"),
            ListItem("Liquid level detector, plays 'Small World' when fluid reaches the probes."),
            ListItem("Hot/near boiling water, from dispenser on counter."),
            ListItem("milk, real or oat, whatever is in the fridge")])
    suppliesList.attrValue('aria-labelledby', suppliesHeading.id())
    oooHeading = Heading(2, "Order Of Operations")
    oooList = OrderedList([ListItem("Collect Supplies"),
            UnorderedList([ListItem("coffee from pantry, 3 packets.  Oh, and the sugar too"),
                ListItem("mug from drying rack"),
                ListItem("scissors from 'junk drawer'")]),
            ListItem("cut tops off coffee packets and empty contents into mug"),
            ListItem("don't forget to throw empty packets in the trash, and put the scissors back where you found them"),
            ListItem("pour one scoop of sugar into mug, make sure no one is  watching how much sugar is used, no need to invite commentary from others"),
            ListItem("add hot water, amount based on listening to how full the mug sounds"),
            ListItem("put level detector on rim of mug"),
            ListItem("add 'milk' until hearing high pitched 'Small World'"),
            ListItem("remove sensor from rim, wipe off probes, put back in drawer"),
            ListItem("stir"),
            ListItem("microwave coffee for 1 minute, the 'milk' cooled it down too much"),
            ListItem("stir again after microwave.  make sure 'milk' is back in the fridge"),
            ListItem("sit on stool at counter, start podcast, enjoy the coffee")])
    oooList.attrValue('aria-labelledby', oooHeading.id())
    detailsHeading = Heading(2, "More Details (because I need to test the dl list)")
    detailsList = DescriptionList([
            DListItem([DesTerm("The Coffee")], DesDef(f"I get the {starbucks} from Amazon as a subscription in the 50 count packet.  That's about as cheap as I can find it")),
            DListItem([DesTerm("The Sugar")], DesDef("It's, I think, the Tabago raw sugar from Trader Joe's.  it looks healthy and sounds exotic")),
            DListItem([DesTerm("Real Milk"), DesTerm("Oat Milk")], DesDef("Why is cow's milk considered 'real'?  Or am I simply calling this out to have multiple <dt> elements for this entry?")),
            DListItem([DesTerm("Why The List?")], DesDef("I don't like having to use a list for dt elements, I should change that interface"))])
    detailsList.attrValue('aria-labelledby', detailsHeading.id())
    props = {
        'title': Title(contents='Lists Test'),
        'mainHeading': Heading(1, "Makin' Coffee, the Coffeenator"),
        'supplies': {
            'heading': suppliesHeading,
            'list': suppliesList
        },
        'orderOfOps': {
            'heading': oooHeading,
            'list': oooList
        },
        'details': {
            'heading': detailsHeading,
            'list': detailsList
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