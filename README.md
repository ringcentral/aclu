# jiraAPI Repo 

This repo is all about using the Jira API to build tools to optimize the usage of Jira from the command line or integrated with home built web apps.

## Jira APIs 

Atlassian has the jira APIs structured in somwhat of a hierarchy.
At the base is the [Jira Server API](https://docs.atlassian.com/software/jira/docs/api/REST/8.18.1/).

The other API of interest  for project management is the 
[Jira Agile API](https://docs.atlassian.com/jira-software/REST/7.3.1/).


## Shell Function 

some bash shell functions are defined in .jirarc. 
They use environment variables for user and password for Jira authentication. 
If you create a file, e.g., .jiraenv which exports those environment variables, remember to chmod 400 .jiraenv to have at least some level of security if you're on a multi user system 

## scripts directory 

this is where Python3 scripts will eventually reside.
There is a requirements.txt file updated with modules required for the scripts.
I suggest using a virtual environment.
I like the command:
'''python 
python3 -m venv --prompt jiraapi .venv 
'''
This will create a virtual environment in a .venv directory and your prompt will be prefixed with "(jiraapi)" once you activate the directory.


