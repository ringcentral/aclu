# Documentation for askJira

askJira was motivated by a need to interface with Jira in a more efficient way, especially when using a screen reader.  
It is primairily a command line tool for searching and presenting data from Jira in a more accessible way.  
That might be command line only with text as output, or web pages might be built with more of a focus on accessibility and navigation when using a screen reader.

## The Atlassian/Jira APIs

Atlassian has the jira APIs structured in somwhat of a hierarchy.
At the base is the
[Jira Server API](https://docs.atlassian.com/software/jira/docs/api/REST/latest/).

The other API of interest  for project management is the
[Jira Agile API](https://docs.atlassian.com/jira-software/REST/latest/).

The board resource in the agile API will be the main focus of the apps.  The board contains epics and sprints which provide paths to issues.  Epics, sprints, and issues are resources themselves and you'll see them as part of the configuration options and output from askJira.  For deeper notes on the Atlassian APIs, see
[notes on Atlassian APIs](jiraApi/ATLASSIAN_API_NOTES.md).

## About the source code

Read it

## Rinning askJira

There is a requirements.txt file updated with modules required for the scripts.
I suggest using a virtual environment.
I like the command:

``` sh
python3 -m venv --prompt askJira  .venv 
```

This will create a virtual environment in a .venv directory and your prompt will be prefixed with "(askJira)" once you activate the directory.

## bash Shell Functions in .jirarc  

some bash shell functions are defined in .jirarc.
I used these when initially trying the Atlassian APIs.
I don't use them any more but thought they might be useful to others.
They're very simple, look in the file for what they do.

Note the environment variables for user and password for Jira authentication.
If you create a file, e.g., .jiraenv which exports those environment variables, remember to `chmod 400 .jiraenv` to have at least some level of security if you're on a multi user system

Also note the host part of the URL is hard coded to jira.ringcentral.com, you probably want to change that.
