# roadmap

## Motivation

The need to track a roadmap spread across multiple Jira epics and backlogs was the initial impetus for the idea of using the REST API to extract information from Jira and present it in static HTML.
A fundamental part of that ability is knowing which epics and backlogs to analyze.
Thus a config file is at the core of the roadmap utility.

## Config File Format

It will initially be kept in a dict in a python file.
Maybe at some point I'll make it more user friendly.  Maybe not.  Maybe YAML.

I'll be iterating on the format for a while so not going to document anything here.
Once I settle on something useful, I'll clarify why it is the way it is.