""" /aclu/uiTest/elementsMdn.py
code to get HTML elements reference from MDN
used by getTableData 

As the HTML reference info is being scraped from the MDN website,
this module is very specific to the layout of the MDN HTML reference pages

As the MDN site is scraped, a TableInfo object is constructed with a row for each element.
The complete TableInfo is returned to be included in who knows/cares what.
"""

import logging 
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup as BSoup 
from bs4.element import Tag 
import json 
from os import path 
import requests 
from typing import Dict 

from ui.elements.utils import Anchor
from ui.builders.tableBuilder  import TableInfo, RowInfo 


elementsReferencePath = "/en-US/docs/Web/HTML/Element"
elementsReferenceBase = f"https://developer.mozilla.org"
elementsReferenceUrl = f"{elementsReferenceBase}{elementsReferencePath}"
mdnAnchor = Anchor(elementsReferenceUrl, "HTML elements reference page on Mozilla Developer Network (MDN)")


#######
def filterAnchor(anchor: Tag) -> bool: 
    """
    for each element, there is a page with a url of the form:
        elementsReferenceUrl/<element_name>
    there are other anchors on the base MDN HTML reference page though with a similar base path
    there is also an anchor with href that looks like its fro an element called 'contributors.txt', filter that out too
    This filter is to ensure we get only the anchors referencing HTML elements 
    """
    href = anchor.attrs.get('href')
    if not href or elementsReferencePath not in href or 'contributors.txt' in href:
        return False 
    elif path.split(href)[0] != elementsReferencePath:
        return False 
    else: return True 


#######
def getElementSummary(soup: BSoup) -> Dict:
    """
    the summary is in the first <p> element immediately after the only <h1> element in the doc
    """
    summary = soup.find('h1').next_sibling.text 
    return  {'summary': summary}


#######
def getElementInfo(name: str, url: str) -> Dict:
    """
    request.get the page for the element 
    then parse it to find what we're looking for 
    """
    print(f'getting info for element {name}')
    elmDoc = requests.get(url)
    elmSoup = BSoup(elmDoc.content, 'html.parser') 
    entries = getElementSummary(elmSoup)
    return entries 


#######
def getElementsData(outfile:str) -> None:
    try:
        refPage = requests.get(elementsReferenceUrl)
        soup = BSoup(refPage.content, 'html.parser')
        anchors = soup.find_all('a')
        elems = list(set([a.attrs.get('href').lower() for a in anchors if filterAnchor(a)]))
        elems.sort()
        print(f'number of element references is {len(elems)}')
        # we have links to each element, 
        # time to scrape each page and create rows for each element 
        table = TableInfo(caption=f'HTML element data scraped from {mdnAnchor}', rowHeadingName='Element')
        for elmPath in elems:
            elmUrl = f'{elementsReferenceBase}{elmPath}'
            elmName = path.split(elmUrl)[1]  
            rowEntries = getElementInfo(elmName, elmUrl)
            row = RowInfo(Anchor(elmUrl, elmName), rowEntries)
            table.addRow(row)
        with open(outfile, 'w') as of:
            tsp = BSoup(str(table.getTable()), "html.parser") 
            of.write(tsp.prettify())
    except Exception as exc:
        logger.exception("something bad happened while scraping MDN")
        return False 
    return True 


## end of file 