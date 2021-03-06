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

def split_message_to_fields(message):
    """Message is in format
    
    message: formatted with last#first#status_of_person#description

    Returns a dictionary
    """
    fields = message.split('#');
    d = {'person_last_name': fields[0],
         'person_first_name': fields[1],
         'note_text': fields[2],
         'person_other': fields[3],
         }
    return d

def convert_datetime_to_rfc3339(dt):
    """Returns RFC 3339 from timestr"""
    time_rfc3339 = vendor.rfc3339.datetimetostr(dt)
    return time_rfc3339

def parse_formatted_message(timestr, source, message):
    """Parse formatted message

    timestr: timestring in the format 2011-05-05 19:30:55
    source: typically a 10 digital phone number
    message: formatted with last#first#description#note

    If note contains alive, dead, missing, seeking, or author,
    the status is updated accordingly.
    """
    #message = 'Koff#Jonathan#Status#Description'
    timestr = str(timestr)
    source = str(source)
    message = str(message)
    fields = split_message_to_fields(message)
    namespace = "rhok1.com"
    unique_id = uuid.uuid1()

    p = Person()
    p.person_record_id = '%s/person.%s' % (namespace, unique_id)

    dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    time_rfc3339 = convert_datetime_to_rfc3339(dt)
    p.entry_date = time_rfc3339
    p.expiry_date = vendor.rfc3339.datetimetostr( dt + datetime.timedelta(12 * 30))
    #dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    #p.entry_date = vendor.rfc3339.datetimetostr(dt)

    p.author_name = source
    p.source_name = source
    p.first_name = fields['person_first_name']
    p.last_name = fields['person_last_name']
    p.other = fields['person_other']

    n = Note()
    n.note_record_id = '%s/note.%s' % (namespace, unique_id)
    n.author_name = source
    p.source_name = source
    n.source_date = p.entry_date
    n.text = fields['note_text']

    if 'alive' in n.text:
        n.status = 'believed_alive'
    elif 'missing' in n.text:
        n.status = 'believed_missing'
    elif 'dead' in n.text:
        n.status = 'believed_dead'
    elif 'seeking' in n.text:
        n.status = 'information_sought'
    elif 'author' in n.text:
        n.status = 'is_note_author'

    p.add_note(n)
 
    return p

def upload_to_personfinder(person):
    """Upload to Google Person Finder """
    action = "write"
    domain = "rhok"
    key = "punsOMMYMAI27tkr"

    url = build_personfinder_url(action, domain, key)
    logging.debug('URL: %s' % url)

    data = to_xml(persons=[person]).toxml().encode('utf8')
    logging.debug('data: %s' % data)
    req = urllib2.Request(
      url, data, { 'Content-Type': 'application/xml' })
    result = None
    result = urllib2.urlopen(req).read()
    logging.debug('return: %s' % result)

    return result

if __name__ == "__main__":
    time = "2011-06-03 19:55:30"
    source = "14154885884"
    message = 'Something#Jonathan#No comments.#Note.'
    upload_to_personfinder(time, source, message)
