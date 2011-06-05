#!/usr/bin/env python
import urllib
import datetime

TROPO = False

# Set up payload
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
source = currentCall.callerID if TROPO else 'debug source'
message = currentCall.initialText if TROPO else 'tinhead#mister#moths in mouth#alive'

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
html = resp.read()

# Output success/failure
if html:
    print "Success"
    print html
    if TROPO:
        if "#" not in message:
            # Send 140 char message for how to use correctly.
            say("Sent to crowd-source for parsing. Please use last_name#first_name#description#update. Update can be: alive, dead, missing, or anything else.")
        else:
            say('Successfully sent')
else:
    print "Failure"
    if TROPO:
        say('Failed send, please send again.')
