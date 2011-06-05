#!/usr/bin/env python
import datetime, time, calendar
import vendor.rfc3339
from communication import send_to_server, upload_to_personfinder

on_tropo = False

now = vendor.rfc3339.now()
time = vendor.rfc3339.datetimetostr(now)
source = currentCall.callerID if on_tropo else "14154885884"
message = currentCall.initialText if on_tropo else "koff#jon#brown shirt#alive"

if "#" not in message:
    # Send freeform message to server for crowdsource uploading
    send_to_server(time, source, message)
else:
    # Put code here to upload directly to PersonFinder
    upload_to_personfinder(message)
