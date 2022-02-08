# Documentation for askJira

askJira was motivated by a need to interface with Jira in a more efficient way, especially when using a screen reader.  
It is primairily a command line tool for searching and presenting data from Jira in a more accessible way.  
That might be command line only with text as output, or web pages might be built with more of a focus on accessibility and navigation when using a screen reader.

## The Atlassian/Jira APIs

Atlassian has the jira APIs structured in somwhat of a hierarchy.
At the base is the
[Jira Server Platform API](https://docs.atlassian.com/software/jira/docs/api/REST/latest/).

The other API of interest  for project management is the
[Jira Software Server (Agile) API](https://docs.atlassian.com/jira-software/REST/latest/).

The board resource in the agile API will be the main focus of the apps.  The board contains epics and sprints which provide paths to issues.  Epics, sprints, and issues are resources themselves and you'll see them as part of the configuration options and output from askJira.  For deeper notes on the Atlassian APIs, see
[notes on Atlassian APIs](jiraApi/ATLASSIAN_API_NOTES.md).

## About the source code

Read it (or wwait for me to fill out this section, don't hold your breath)

## Rinning askJira

There is a requirements.txt file updated with modules required for the scripts.
I suggest using a virtual environment.
I like the command:

``` sh
python3 -m venv --prompt askJira  .venv 
```

This will create a virtual environment in a .venv directory and your prompt will be prefixed with "(askJira)" once you activate the environment:
""" sh
source ./venv/bin/activate
"""

With the virtual environment setup, run:
""" sh
pip install -r requirements.txt
"""
Now you are set to run askJira.  I've tried to add enough help in the project to avoid having to write it here.  Try running:
""" sh
python askJira.py --help
"""
for the command line arguments and options.  As of Feb 8, 2022, there are two commands, "server" and "agile."  You should see the list of commands in the output from --help.  For options for commands try, for example:
""" sh
python askJira.py agile --help
"""

askJira needs your Jira credentials for basic authentication for the REST API requests.  askJira will look for those in environment variables "JIRA_USER" and "JIRA_PW."
Alternatively, you can use command line options (as seen in the --help output) or askJira will ask you for the values as a last resort.  Your password will not be echoed on the screen if you opt for the last resort.

## Config File

Instead of using askJira to search Jira, you can specify a config file with information you know you want.
See the file "ajConfig.json" for notes about the config file.

## bash Shell Functions in .jirarc  

some bash shell functions are defined in .jirarc.
I used these when initially trying the Atlassian APIs.
I don't use them any more but thought they might be useful to others.
They're very simple, look in the file for what they do.

Note the environment variables for user and password for Jira authentication.
If you create a file, e.g., .jiraenv which exports those environment variables, remember to `chmod 400 .jiraenv` to have at least some level of security if you're on a multi user system

Also note the host part of the URL is hard coded to jira.ringcentral.com, you probably want to change that.
