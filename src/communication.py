#!/usr/bin/env python
import urllib
import datetime, time, calendar
import vendor.rfc3339

def send_to_server(time, source, message):
    # make a dictionary of search parameters
    q = {'source': source,
        'message': message,
        'time': time}
    
    # encode the http string
    query = urllib.urlencode(q)

    url="http://smspersonfinder.appspot.com/create?%s" % query
     
    print "Opening %s" % url
    resp = urllib.urlopen(url)
    html = resp.read()
    if html:
        if on_tropo:
            say('Successfully submitted.')
        else:
            print "Success"
            print html
    else:
        if on_tropo:
            say('Failure, please submit again')
        else:
            print "Failure"

if __name__ == "__main__":
    on_tropo = False

    now = vendor.rfc3339.now()
    time = vendor.rfc3339.datetimetostr(now)
    source = currentCall.callerID if on_tropo else "14154885884"
    message = currentCall.initialText if on_tropo else "koff#jon#brown shirt#alive"

    send_to_server(time, source, message)
    if "#" not in message:
        # Send to server for crowdsource uploading
        send_to_server(time, source, message)
    else:
        # Put code here to upload directly to PersonFinder
        pass
