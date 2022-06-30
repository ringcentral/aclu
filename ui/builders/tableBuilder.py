""" aclu/ui/builders/tableBuilder.py

the tableBuilder module is the first attempt at providing some level of abstraction to creating a more complicated HTML element 
dataclasses are used to represent HTML table related elements using any datatypes 
RowInfo and TableInfo objects have properties with semantics indicating their use within the table
The specific HTML elements used to construct the table are encapsulated within the classes  

The user can create the rows however they like then add them to the TableInfo object
"""

from dataclasses import dataclass, field  
from typing import Any, Dict, List  

from ..elements.tables import Caption, Table, TableRow, TableData, TableColumnHeader, TableRowHeader, TableHead, TableBody     


#######
@dataclass
class RowInfo:
    """
    RowInfo has the values for the cells of the row stored as a dict (with the row heading called out separately) 
    the key in the entries dict is the column name, the value is what will eventually be in the <th> or <td> elements
    the first item is called out as the heading for that row mainly as an API feature.
    """
    heading: Any = 'you need to set the row heading'
    entries: Dict = field(default_factory=dict)  # this is how **kwArgs works in dataclasses 

    #####
    def addEntries(self, **kwArgs) -> None:
        """
        add entries to the row by passing in any number of named parameters (columnname = 'some value').
        the names represent the columns,
        the value is the entry in that column for this row 
        """
        self.entries.update(kwArgs)

    #####
    def properties(self) -> List[Any]:
        """
        the properties are the column headings for the table 
        the value for each cell in the row is stored in a dict with the property (key) being the column for that value 
        """
        return list(self.entries.keys())

    def getRow(self, columns: List[Any]) -> TableRow:
        """
        return the TableRow object that can generate the HTML for the row 
        the columns parameter is needed to know which values from entries to include in the row 
        """
        rowCells =[TableRowHeader(self.heading)]
        rowCells += [TableData(self.entries.get(col)) for col in columns]
        """
        rowCells is now a list of Elements (representing <th> and <td> elements)
        it can be used to create a TableRow (representing a <tr> element) object 
        """
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

    #####
    def addRow(self, row: RowInfo) -> None:
        self.rows.append(row) 

    #####
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

    #####
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
        """
        split this to multiple lines for readability 
        first add the table head <th> element to the table.
        a <th> is a list of rows though in this case it's a single row of the names of the columns
        a TableRow is a list of anything derived from TableData <td> or TableHeader <th> elements 
        """
        table.addElement(
            TableHead([
                TableRow(
                    [TableColumnHeader(colName) for colName in columnNames]  # list comprehension to initiate the TableRow 
                )  # close of TableRow construction 
            ])  # close TableHead construction including close list for list of TableRows to construct TableHead 
        )  # close of addElement 
        """
        now add all the rows in the tbody element 
        same idea as adding the TableHead above 
        """
        table.addElement(TableBody([row.getRow(self.columnHeadings) for row in self.rows]))
        return table


#######
def createTableFromDicts(caption: Any, rows: List[Dict]) -> Table:
    """
    this is, so far, the easiest way to construct an HTML table from data the user has pulled from anywhere
    The rows are the dicts in the list, in order they appear in the list
    the column names are derived from the keys in the dicts
    the row heading is the first item in the dict 
    and the column heading for the first column in the table is the first key in the dict for the row

    Using this a developer doesn't need to know anything about generating HTML tables, especially accessibility 
    it's all about defaults...
    """
    rowHeadingName = list(rows[0].keys())[0]
    tableinfo = TableInfo(caption, rowHeadingName)
    for row in rows:
        items = list(row.items())
        heading = items[0][1]
        entries = dict(items[1:])
        ri = RowInfo(heading, entries)
        tableinfo.addRow(ri)
    return tableinfo.getTable()


## end of file 