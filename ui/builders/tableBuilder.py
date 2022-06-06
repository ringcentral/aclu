""" aclu/ui/builders/tableBuilder.py

the tableBuilder module is the first attempt at providing some level of abstraction to creating a more complicated HTML element
The attempt is to present the table simply as rows of entries
The user can create the rows however they like then add them to the TableInfo object

A Row class is used to encapsulate how a row is constructed 
"""

from dataclasses import dataclass, field  
from typing import Any, Dict, List  

from ..elements.tables import Caption, Table, TableRow, TableData, TableColumnHeader, TableRowHeader, TableHead, TableBody     


#######
@dataclass
class RowInfo:
    """
    TableInfo holds a list of items that can be used as content in th or td elements
    the first item is called out as the heading for that row mainly as an API feature.
    It could have just been the 0th element of entries.
    """
    heading: Any = 'default row heading'
    entries: Dict = field(default_factory=dict)

    def addEntries(self, **kwArgs) -> None:
        """
        add entries to the row by passing in any number of named parameters (columnname = 'some value').
        the names represent the columns,
        the value is the entry in that column for this row 
        """
        self.entries.update(kwArgs)

    def properties(self) -> List[Any]:
        """
        the properties are the column headings for the table 
        the value for each cell in the row is stored in a dict with the property being the column for that value 
        """
        return self.entries.keys()

    def getRow(self, columns: List[Any]) -> TableRow:
        """
        return the TableRow object that can generate the HTML for the row 
        the columns parameter is needed to know which values from entries to include in the row 
        """
        rowCells =[TableRowHeader(self.heading)]
        rowCells += [TableData(self.entries.get(col)) for col in columns]
        return TableRow(rowCells)


#######
@dataclass
class TableInfo:
    """
    an object of TableInfo holds all the information needed to generate an HTML table
    """
    caption: Any 
    rowHeadingName: Any = 'Row Names' # the 0th column, i.e., the column of row headings  
    columnHeadings: List[Any] = field(default_factory = list)
    rows: List[RowInfo] = field(default_factory= list)

    def addRow(self, row: RowInfo) -> None:
        self.rows.append(row) 

    def generateColumnHeadings(self):
        """
        if you don't want to set the column headings directly, they can be inferred by the names of properties in the rows

        this method will iterate through the rows and keep track of the property name of each item in a row
        The columns can then be arranged based on the position of the propertys in the rows (the default),
        or another option can be specified (TODO) 
        """        
        counts = {}
        for row in self.rows:
            for prop in row.properties():
                if not counts.get(prop): counts[prop] = 1
                else: counts[prop] += 1
        # for now, column headings are all the properties found in the rows
        # TODO: allow the user to specify ordering of the columns based on counts 
        #    or maybe columnHeadings.sort() 
        self.columnHeadings = list(counts.keys()) 

    #######
    def getTable(self) -> Table:
        """
        need to go through self (TableInfo) and convert all the info 
        to corresponding elemensts (tr, th, td, caption...)
        """
        table = Table(Caption(self.caption))
        # first add the column headings to the table 
        # if column headings hve not been set yet, generate them based on the  rows 
        if len(self.columnHeadings) == 0: self.generateColumnHeadings()
        columnNames = [self.rowHeadingName] + self.columnHeadings
        table.addElement(TableHead([TableRow([TableColumnHeader(colName) for colName in columnNames])]))
        # now add all the rows in the tbody element 
        table.addElement(TableBody([row.getRow(self.columnHeadings) for row in self.rows]))
        return table


## end of file 