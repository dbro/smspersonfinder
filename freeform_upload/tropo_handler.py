#!/usr/bin/env python
import urllib
import datetime

TROPO = False

# Set up payload
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
source = currentCall.callerID if TROPO else 'debug source'
message = currentCall.initialText if TROPO else 'appleseed#johnny#pan on head#alive'

# Build query string
q = {'source': source,
    'message': message,
    'time': time}

query = urllib.urlencode(q)

# Deliver payload
url="http://smspersonfinder.appspot.com/create?%s" % query
if not TROPO:
    print "Opening %s" % url
resp = urllib.urlopen(url)
html = resp.read()

# Output success/failure
if html:
    print "Success"
    print html
    if TROPO:
        say('Successfully sent')
else:
    print "Failure"
    if TROPO:
        say('Failed send, please send again.')
