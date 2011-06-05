#!/usr/bin/env python

import message
import urllib2

def build_url(action, domain, key):
    """
    Action is write/note/person
    """
    url = "https://%s.googlepersonfinder.appspot.com/api/%s?key=%s" % (domain, action, key)
    return url

if __name__ == "__main__":
    domain = "rhok"
    key = "punsOMMYMAI27tkr"
    action = "write"
    sms = 'Koff#Jonathan#No comments.'
    namespace = "rhok1.com"

    url = build_url(action, domain, key)
    fmtd_msg = message.FormattedMessage(namespace, sms)

    req = urllib2.Request(
      url, fmtd_msg.serializeAsPFIF(), { 'Content-Type': 'application/xml' })
    print urllib2.urlopen(req).read()
