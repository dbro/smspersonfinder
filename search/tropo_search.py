#!/usr/bin/env python

import urllib2
import urllib

answer()

Domain = "smspersonfinder.appspot.com"

OriginNumber = currentCall.callerID

# Current implementation: name[,dob(MM/DD/YY),address]
IncomingMessage =  currentCall.initialText 

URI = "/search?message=%s" % IncomingMessage
Query = urllib.urlencode("%s%s" % (domain, URI))

# Retrieve result from GET
result = urllib2.urlopen(Query).read()

# Send text message response
event = call([OriginNumber], {"network":"SMS", "channel":"TEXT"})
event.value.say(result)
