import urllib2

SUBDOMAIN = 'rhok'
url = "https://googlepersonfinder.appspot.com/api/search?key=%s&subdomain=%s&q=%s"
req = urllib2.urlopen(url % ('', SUBDOMAIN, 'Jon'))
print req.read(1000000)

str = 'Koff#Jonathan#No comments.'
fields = str.split('#')

print """
<?xml version="1.0" encoding="UTF-8"?> 
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3"> 
  <pfif:person> 
    <pfif:person_record_id>rhok.person-finder.appspot.com/person.113147</pfif:person_record_id> 
    <pfif:first_name>%(first_name)s</pfif:first_name> 
    <pfif:last_name>%(last_name)s</pfif:last_name> 
    <pfif:other>description:
%(comments)s
    </pfif:other> 
  </pfif:person> 
</pfif:pfif>
""" % {'first_name': fields[1], 'last_name': fields[0], 'comments': fields[2]}
