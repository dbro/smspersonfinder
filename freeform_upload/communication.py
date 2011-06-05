#!/usr/bin/env python
# for send_to_server
import urllib
# for upload_to_server
from models import *
from util import *
import datetime, time, calendar
import vendor.rfc3339
import urllib2
import time
import uuid

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

def parse_formatted_message(timestr, source, message):
    """Parse formatted message

    timestr: timestring in the format 2011-05-05 19:30:55
    source: typically a 10 digital phone number
    message: formatted with last#first#description#note
    """
    #message = 'Koff#Jonathan#No comments.#Note.'
    timestr = str(timestr)
    source = str(source)
    message = str(message)
    fields = message.split('#');
    namespace = "rhok1.com"
    unique_id = uuid.uuid1()

    p = Person()
    p.person_record_id = '%s/person.%s' % (namespace, unique_id)

    dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    p.entry_date = vendor.rfc3339.datetimetostr(dt)
    p.expiry_date = vendor.rfc3339.datetimetostr(
      dt + datetime.timedelta(12 * 30))

    p.author_name = source
    p.source_name = source
    p.first_name = fields[1]
    p.last_name = fields[0]
    p.other = fields[2]

    n = Note()
    n.note_record_id = '%s/note.%s' % (namespace, unique_id)
    n.author_name = source
    p.source_name = source
    n.source_date = p.entry_date
    n.text = fields[3]
    p.add_note(n)
 
    return p

def upload_to_personfinder(person):
    """Upload to Google Person Finder """
    action = "write"
    domain = "rhok"
    key = "punsOMMYMAI27tkr"

    url = build_personfinder_url(action, domain, key)

    data = to_xml(persons=[person]).toxml()
    req = urllib2.Request(
      url, data, { 'Content-Type': 'application/xml' })
    result = urllib2.urlopen(req).read()
    return result

if __name__ == "__main__":
    time = "2011-06-03 19:55:30"
    source = "14154885884"
    message = 'Something#Jonathan#No comments.#Note.'
    upload_to_personfinder(time, source, message)
