#!/usr/bin/python

from datetime import datetime
import pytz

print datetime.utcnow()

#indatestr = "2018-07-28 02:57:58 +0000"
indatestr = "2018-07-28 02:57:58"

dt   = datetime.strptime (indatestr, "%Y-%m-%d %H:%M:%S")
outdate   = datetime.strftime ("%Y-%m-%d %H:%M:%S +0000", dt)
print outdate
