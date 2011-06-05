#!/usr/bin/env python
import urllib
import datetime
import twilio

TROPO = False 
NUMFIELDS = 4

# Twilio account
API_VERSION = '2010-04-01'
ACCOUNT_SID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCOUNT_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
CALLER_ID = '000-000-0000' 

def test_call():
    d = {
        'From' : CALLER_ID,
        'To' : '000-000-0000',
        'Url' : 'http://demo.twilio.com/welcome',
    }
    try:
        print account.request('/%s/Accounts/%s/Calls' % (API_VERSION, ACCOUNT_SID), 'POST', d)
    except Exception, e:
        print e
        print e.read()

def send_sms(message):
    d = {
        'From' : CALLER_ID,
        'To' : '000-000-0000',
        'Body' : message
    }
    try:
        print account.request('/%s/Accounts/%s/SMS/Messages' % (API_VERSION, ACCOUNT_SID), 'POST', d)
    except Exception, e:
        print e
        print e.read()

account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

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
url="http://smspersonfinder.appspot.com/create?%s" % query
if not TROPO:
    print "Opening %s" % url
resp = urllib.urlopen(url)
result = resp.read()

# Output success/failure
if result:
    print "Success"
    print result
    if TROPO:
        say(message)
    else:
        send_sms(message)
else:
    print "Failure"
    if TROPO:
        say('Send failed, please try again.')
    else:
        send_sms("Failure") 
