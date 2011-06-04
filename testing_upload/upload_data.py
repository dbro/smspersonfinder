#!/usr/bin/env python

import urllib2

def build_url(action, domain, key):
    """
    Action is write/note/person
    """
    url = "https://%s.googlepersonfinder.appspot.com/api/%s?key=%s" % (domain, action, key)
    return url

def build_request_body(formatted_msg, namespace):
    # Formatted message format: Last#First#Comment
    fields = formatted_msg.split('#')
    return """
    <?xml version="1.0" encoding="UTF-8"?> 
    <pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3"> 
      <pfif:person> 
        <pfif:person_record_id>%(namespace)s/person.113147</pfif:person_record_id> 
        <pfif:first_name>%(first_name)s</pfif:first_name> 
        <pfif:last_name>%(last_name)s</pfif:last_name> 
        <pfif:other>description:
%(comments)s
        </pfif:other> 
      </pfif:person> 
    </pfif:pfif>
    """ % {
      'first_name': fields[1],
      'last_name': fields[0],
      'comments': fields[2],
      'namespace': namespace
    }

if __name__ == "__main__":
    domain = "rhok"
    key = "punsOMMYMAI27tkr"
    action = "write"
    namespace = "rhok1.com"

    url = build_url(action, domain, key)
    print url

    data = build_request_body('Koff#Jonathan#No comments.', namespace)
    req = urllib2.Request(url, data)
    print urllib2.urlopen(req).read()
