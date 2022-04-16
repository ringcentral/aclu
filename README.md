# Accessible Command Line Utilities (ACLU)

This repo contains utilities with a broad theme of making tasks developers often perform more efficient when using a screen reader.

## searchjira 

Every developer knows of the fundamental need to track work to be done on their project.  jira has become a defacto standard tool in the software developement industry.  Thus the first utility created is focused on finding information in Jira.

[Documentation for searchjira](searchjira/README.md)

## jiraApi

JiraApi contains the definition of a class encapsulating the Jira APIs.
It's in its own package partly so I can use it in the Python repl.

Check out the 
[README for the jiraApi](jiraApi/README.md)
for some details regarding the Atlassian APIs.

## roadmap

This is another tool used to access and aggregate information from Jira.
The idea is a team's roadmap might be spread across multiple agile constructs, e.g., epics and backlogs.
That information can be specified in a config file and roadmap can be run to easily get a snapshot of the status of the roadmap.
see the README for a description of the config file.

[Documentation (README) for roadmap](roadmap/README.md)

## ui

this package is the code and templates used to generate HTML pages with data gathered by the command line tools.
This is evolving and I'm not quite sure yet how it will be used by the different tools.

[README for the ui package.](ui/README.md)

## Rinning aclu tools

There is a requirements.txt file in the root aclu directory with modules required for the scripts.
I suggest using a virtual environment if you clone this repo and want to develope an run the tools locally.
I like the command:

``` sh
python3 -m venv --prompt aclu .venv 
```

This will create a virtual environment in a .venv directory and your prompt will be prefixed with "(aclu)" once you activate the environment:
``` sh
source ./venv/bin/activate
```

With the virtual environment setup, run:
``` sh
pip install -r requirements.txt
```
Now you are set to run the aclu tools.  I've tried to add enough help in the project to avoid having to write it here.  Try running:
``` sh
python3 -m  searchjira --help
```
for the command line arguments and options.  
You should see the list of commands in the output from --help.  For options for commands try, for example:
``` sh
python3 -m searchjira boards--help
```

## Jira Configuration

### Credentials

Any of the tools using Jira  will need your Jira credentials for basic authentication for the REST API requests.  
Those can be configured in environment variables "JIRA_USER" and "JIRA_PW."
Alternatively, you can use command line options (as seen in the --help output) or the tool will ask you for the values as a last resort.  Your password will not be echoed on the screen if you opt for the last resort.

### Jira URL 

Similar to the credentials, the base URL for the Jira APIs is needed by any tool using Jira.
The base URL can be set in an environment variable, JIRA_BASE_URL, on the command line, or entered when asked by the program.

The base URL should only be the domain, e.g, https://jira.mycompany.com.  You might need to ask your Jira admin how to access the APIs.

