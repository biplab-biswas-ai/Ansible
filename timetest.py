#!/usr/bin/env python2

import datetime
import json

date = str(datetime.datetime.now())
print json.dumps({
    "time" : date
})
