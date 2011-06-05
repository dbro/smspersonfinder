#!/usr/bin/env python
# for send_to_server
import urllib
# for upload_to_server
from models import *
from util import *
import datetime, time, calendar
import vendor.rfc3339
import urllib2

def send_to_server(time, source, message):
    """Useless, because we're already on the server"""
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
        print "Success"
        print html
    else:
        print "Failure"

def build_personfinder_url(action, domain, key):
    """
    Action is write/note/person
    """
    url = "https://%s.googlepersonfinder.appspot.com/api/%s?key=%s" % (domain, action, key)
    return url

def upload_to_personfinder(sms):
    #sms = 'Koff#Jonathan#No comments.#Note.'
    domain = "rhok"
    key = "punsOMMYMAI27tkr"
    action = "write"
    namespace = "rhok1.com"

    fields = sms.split('#');
    p = Person()
    p.person_record_id = namespace + '/' + 'person.123456';
    now = vendor.rfc3339.now()
    p.entry_date = vendor.rfc3339.datetimetostr(now)
    p.expiry_date = vendor.rfc3339.datetimetostr(
      now + datetime.timedelta(12 * 30))
    p.author_name = 'Unknown'
    p.first_name = fields[1]
    p.last_name = fields[0]
    p.description = fields[2]

    n = Note()
    n.note_record_id = namespace + '/' + 'note.123456'
    n.author_name = 'Unknown'
    n.source_date = p.entry_date
    n.text = fields[3]
    p.add_note(n)
    
    url = build_personfinder_url(action, domain, key)
    #fmtd_msg = message.FormattedMessage(namespace, sms)

    data = to_xml(persons=[p]).toxml()
    req = urllib2.Request(
      url, data, { 'Content-Type': 'application/xml' })
      #url, fmtd_msg.serializeAsPFIF(), { 'Content-Type': 'application/xml' })
    result = urllib2.urlopen(req).read()
    print result
    return result

