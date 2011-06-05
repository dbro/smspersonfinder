#!/usr/bin/env python
import urllib
import datetime

TROPO = False
NUMFIELDS = 4

# Set up payload
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
source = currentCall.callerID if TROPO else 'debug source'
message = currentCall.initialText if TROPO else 'tinhead#mister#moths in mouth#missing'

# Build query string
q = {'source': source,
    'message': message,
    'time': time}

query = urllib.urlencode(q)

# Deliver payload
if TROPO:
    url="http://smspersonfinder.appspot.com/create?%s" % query
else:
    url="http://localhost:8080/create?%s" % query
if not TROPO:
    print "Opening %s" % url
resp = urllib.urlopen(url)
result = resp.read()

# Output success/failure
if result:
    print "Success"
    print result
    if TROPO:
        say(result)
else:
    print "Failure"
    if TROPO:
        say('Send failed, please try again.')
