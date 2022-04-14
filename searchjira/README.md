# Documentation for searchjira

searchjira was motivated by a need to interface with Jira in a more efficient way, especially when using a screen reader.  
It is primairily a command line tool for searching and presenting data from Jira in a more accessible way.  
That might be command line only with text as output, or HTML documents might be created from the data with more of a focus on accessibility and navigation when using a screen reader.

## Rinning searchjira

See the notes in the aclu root README regarding configuration of Jira credentials and URL.

searchjira can be run as a module from any version of Python3.7 and above.  Make sure you have the modules specified in the requirements .txt file.  See the root README in aclu for notes regarding using a virtual environment.

``` sh 
python3 -m searchjira --help 
```
