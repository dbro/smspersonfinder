#!/usr/bin/env python

import urllib2
import urllib

answer()

Domain = "http://smspersonfinder.appspot.com"
Path = "/search?"

OriginNumber = currentCall.callerID

# Current implementation: name[,dob(MM/DD/YY),address]
IncomingMessage =  currentCall.initialText 
QueryArgs = { 'message':IncomingMessage }

URI = urllib.urlencode(QueryArgs)
Query = "%s%s%s" % (Domain, Path, URI)

# Retrieve result from GET
result = urllib2.urlopen(Query).read()

# Send text message response
event = call([OriginNumber], {"network":"SMS", "channel":"TEXT"})
event.value.say(result)
