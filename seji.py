#!/usr/bin/env python
"""  aclu/seji.py 
this small script is to avoid typeing 
python -m searchjira ...
each time
"""

import logging 
## import jsonloggeriso8601datetime 

from searchjira import run 

if __name__ == '__main__':
    run()

    ## end of file 