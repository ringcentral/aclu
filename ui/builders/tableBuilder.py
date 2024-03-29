""" aclu/ui/builders/tableBuilder.py

The tableBuilder module is the first attempt at providing some level of abstraction to creating a more complicated HTML element. 
dataclasses are used to represent HTML table related elements using any datatypes. 
RowInfo and TableInfo objects have properties with semantics indicating their use within the table.
The specific HTML elements used to construct the table are encapsulated within the classes.  

The user can create the rows however they like then add them to the TableInfo object.

There is a necessary correlation between the dict defining the row and dict defining the column headings in the TableInfo.
That correlation is in the keys of the dicts.
The dict defining the column headings defines which values within a row are included in the table.
Thus a row can be a dict with an arbitrary list of key, value pairs.
Then what is included in a table is defined by the column headings dict.
When a table is being generated from TableInfo,
the keys from the column headings dict is sent to each RowInfo.
The RowInfo object uses that to get the value for the cell for that column.
If the RowInfo entries dict has a matching key, the associated value is used for that cell (a <td> element.)
If there is no matching key, the cell will be empty (or use None) for that row for that column .

The values in the column headings dict can be used to have custom names for the column headings. 
The default name of the column heading is the key itself, e.g.:
columnHeadings = {'col1':'col1', 'col2':'col2', ... }
"""

from dataclasses import dataclass, field  
from typing import Any, Dict, List  

from ..elements.tables import Caption, Table, TableRow, TableData, TableColumnHeader, TableRowHeader, TableHead, TableBody     


#######
@dataclass
class RowInfo:
    """
    RowInfo has the values for the cells of the row stored as a dict (with the row heading called out separately) 
    the key in the entries dict is the column id, the value is what will eventually be in the <th> or <td> elements
    the first item is called out as the heading for that row mainly as an API feature.
    """
    heading: Any = 'you need to set the row heading'
    entries: Dict = field(default_factory=dict)  # this is how **kwArgs works in dataclasses 

    #####
    def addEntries(self, **kwArgs) -> None:
        """
        add entries to the row by passing in any number of named parameters (columnId = 'some value').
        the Ids represent the columns,
        the value is the entry in that column for this row 
        """
        if self.entries: self.entries.update(kwArgs) 
        else: self.entries = kwArgs 

    #####
    def properties(self) -> List[Any]:
        """
        the properties are the column heading ids for the table 
        the value for each cell in the row is stored in a dict with the property (key) being the column for that value 
        """
        if self.entries: return list(self.entries.keys())
        else: return []

    #####
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
    columnHeadings: Dict = field(default_factory=dict)  
    # columnHeadings: List[Any] = field(default_factory = list)
    # customColumnHeadings: List[Any] = field(default_factory = list)
    rows: List[RowInfo] = field(default_factory= list)

    #####
    def addRow(self, row: RowInfo) -> None:
        self.rows.append(row) 

    #####
    def generateColumnHeadings(self) -> None:
        """
        if you don't want to set the column headings directly, they can be inferred by the names of properties in the rows

        this method will iterate through the rows and keep track of the property name (key) of each item (key, value pair) in a row
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
        # self.columnHeadings = list(counts.keys()) 
        self.columnHeadings = { key:key for key in counts.keys()}

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
        columnNames = [self.rowHeadingName] + list(self.columnHeadings.values())
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
        table.addElement(TableBody([row.getRow(list(self.columnHeadings.keys())) for row in self.rows]))
        return table


#######
def createTableFromDicts(caption: Any, rows: List[Dict]) -> Table:
    """
    this is, so far, the easiest way to construct an HTML table from data the user has pulled from anywhere
    The rows are the dicts in the list, in order they appear in the list
    the column names are derived from the keys in the dicts
    the row heading is the value from the first item in the dict representing that row  
    and the heading for the first column (column of row headings) in the table is the key from the first key, value  pair from the first dict in the list 

    Using this a developer doesn't need to know anything about generating HTML tables, especially accessibility 
    it's all about defaults...
    Caveat, I've only used this for lists of very consistent dicts,
    that is, they all have the same size and keys.
    It's likely this fails quickly for random dicts in a list 
    That is, if the dicts represent, say a very sparsely populated table, dicts with different keys with little overlap 
    this table might not be what you want.
    It's better to use the TableInfo and RowInfo dataclasses 
    """
    if len(rows) == 0: raise ValueError('no rows sent to createTableFromDict')
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