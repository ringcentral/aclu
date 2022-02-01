## The Atlassian/Jira APIs 

Atlassian has the jira APIs structured in somwhat of a hierarchy.
At the base is the [Jira Server API](https://docs.atlassian.com/software/jira/docs/api/REST/latest/).

The other API of interest  for project management is the 
[Jira Agile API](https://docs.atlassian.com/jira-software/REST/latest/).

 
## About the source code 

Read it 

## Rinning askJira 

There is a requirements.txt file updated with modules required for the scripts.
I suggest using a virtual environment.
I like the command:
```
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

