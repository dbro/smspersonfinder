#!/usr/bin/env python

import urllib2
import urllib

answer()

Domain = "http://smspersonfinder.appspot.com"
Path = "/search?"

OriginNumber = currentCall.callerID

def send_to_appengine(msg):
	QueryArgs = { 'message':msg }
	URI = urllib.urlencode(QueryArgs)
	Query = "%s%s%s" % (Domain, Path, URI)

	# Return result from GET
	return urllib2.urlopen(Query).read()

def message_user(msg, keepalive):
	if not keepalive:
		event = call([OriginNumber], {"network":"SMS", "channel":"TEXT"})
		event.value.say(msg)
		hangup()
	else:
		pass

def text_call_handler():
	# Current implementation: name[,dob(MM/DD/YY),address]
	IncomingMessage =  currentCall.initialText 
	response = send_to_appengine(IncomingMessage)
	message_user(response, False)


def voice_call_handler():
	say("Sorry, voice calls are not supported. Please send an SMS message instead.")
	hangup()

if currentCall.channel == "SMS":
	text_call_handler()
elif currentCall.channel == "VOICE":
	voice_call_handler()
