# Going Slightly Deeper into the Atlasssian APIs

## Start at the Beginning?

If you're new to the Atlassian APIs, you might want to start at the very beginning:
[developer.atlassian.com](https://developer.atlassian.com/).

On the other hand, it took me a while to sort out the terminology.  Maybe my processing speed is a little slow, and the Atlassian developer docs will be intuitively obvious to you.  If all you care about though is the REST APIs, you might do well to stick to this overview, at least initially.

### Terminology

In the Atlassian developer docs, you'll come across the terms app, API, REST, SDK, framework, Java, Jsp, server, data center, cloud, marketplace, and certainly others I've missed.  Each term means something to me, some more or less abstract than others, but when used in context of the developer docs, I was initially confused.  Here's what I eventually realized.

Atlassian products (Jira, Confluence, etc) can be deployed locally in a customer's data center or some clould infrastructure managed by the customer, or customers can signup for services hosted by Atlassian.  The self hosted deployment is referred to as Server or Data Center.  The Server option is transitioning to the Data Center option.  No more Server licenses are being sold and the Server product itself is end of support February 2nd, 2024.  Going forward, Data Center is the product Atlassian sells for anyone needing to manage their own systems.

The recommended approach is for customers to sign up for Atlassian Cloud and use products hosted by Atlassian.  This is the SAAAS approach.

much of the developer documentation focuses on developing and deploying apps to be offered to other Atlassian customers.  How you do that for Data Center deployments vs Cloud is different with different options for both development and deployment.  For example, in one case the Java API should be used, in another case, use JSP.  As I was initially reading through this, I wondered what does all this have to do with the REST APIs and wht I want to do?

The short answer is, nothing, or at least very little, and I was going down the wrong rabbit hole.

### What About My Needs?

Conceptually, I wanted to use Jira as a database.  Querying that database is done via HTTPS GET requests (e.g., a REST API).  I didn't want to deploy my "app" on Jira cloud or sell it to other Atlassian users.  Once I achieved enlightenment, that the docs were more about an Atlassian App Store, I could cut through the cruft and focus on the REST APIs.

## The REST APIs

From the developer main page,
[developer.atlassian.com](https://developer.atlassian.com/),
look for "Explore the docs" (heading level2).  In that section are two buttons, one for Cloud, the other for Server (which is called Data Center now).  I'm focused on the self hosted product so I click on the Server button.

Now I'm presented with a bunch of level 3 headings for the various Atlassian products.  The first heading is for the Jira Server Platform API.  "The Jira platform has functionality common to all Jira products."  There is a link at the end of that heading  section to the REST API documentation for the Jira Platform Server.
[latest version of the Jira Server Platform REST API docs](https://docs.atlassian.com/software/jira/docs/api/REST/latest/)

The very next level 3 heading  is for the Jira Software Server (also referred to as the Jira Agile API in other places in the Atlassian docs).  Look for the link to the REST API at the end of the heading section.
[latest version of the Jira Software Server REST API](https://docs.atlassian.com/jira-software/REST/latest/)

### Pagination

For many of the types of resources in a Jira deployment, there can be very large numbers of instances.
Think of how many issues  there would be in even a small companies Jira deployment.  If you tried to GET all issues from Jira in a single GET request, the payload would be huge.  Most likely something would timeout.  Thus, many of the resources are returned in "pages."

Pagination is described in the documentation for each of the REST APIs.  Unfortunately, there are some inconsistencies in the implementations making it difficult to provide a generic utility to GET all paginated resources.
I initially decided to let different areas of the code deal with pagination, and the differences, instead of trying to account for them in one place.
This turned in to much more code redundancy than ugliness of accounting for the differences in one, encapsulated place.

I'm not documenting the differences here, I think the code is good enough to understand.  
Check out the file
[jiraApiUtils.py](jiraApiUtils.py)

## Wrapping Up, Things to Remember

I'm initially focused on getting project tracking information from Jira (the Agile API) so I'll stop here.  Keep in mind though there are REST APIs for most of the other Atlassian products as well.  You can see those in the remaining level 3 headings and go to their respective APIs folowing the links in each section.
