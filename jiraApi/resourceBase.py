"""  aclu/jiraApi/resourceBase.py 
establishing a resource base initially for the get*() funtion each of the Jira resources has 
It might not end up with any more than that...
"""


import logging 
logger = logging.getLogger(__name__)

from typing import Dict 

from . import jiraApiUtils 

#######
class ResourceBase:
    @classmethod
    def get(cls, resourceUrl: str, resourceId: str) -> object:
        """
        this get is used by all resources extending ResourceBase to 
        get the resource from Jira
        the URL must be fully constructed by the calling method
        the resourceId is used only for logging support 
        """
        resp, resource = jiraApiUtils.getResource(resourceUrl, convertPayload=True)
        if resource is None:
            logger.info(f'could not find resource with id: {resourceId}')
            return None 
        else:
            return cls(resource)


## end of file 