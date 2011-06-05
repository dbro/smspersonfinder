import urllib2
from models import *
from util import *

SubDomain = "rhok"
AuthToken = "soNQ67BhLRP0tIvP"
query = "brown" 
query_uri = "/api/search?key=" + AuthToken + "&subdomain=" + SubDomain + "&q=" + query
host = "https://googlepersonfinder.appspot.com"

def name_search(name, persons):
    found_persons = []
    name = name.lower()

    for person in persons:
        full_name = person.full_name
        first_name = person.first_name
        last_name = person.last_name

        if full_name and full_name.lower().find(name):
            found_persons.append(person)
            continue
        elif first_name and first_name.lower().find(name):
            found_persons.append(person)
            continue
        elif last_name and last_name.lower().find(name):
            found_persons.append(person)
            continue

    return found_persons

def format_info(person) :
    return person.first_name + person.last_name

def print_full_info(person) :
    print "person_record_id..%s" % person.person_record_id
    print "entry_date........%s" % person.entry_date
    print "expiry_date.......%s" % person.expiry_date
    print "author_name.......%s" % person.author_name
    print "author_email......%s" % person.author_email
    print "author_phone......%s" % person.author_phone
    print "source_name.......%s" % person.source_name
    print "source_date.......%s" % person.source_date
    print "source_url........%s" % person.source_url
    print "full_name.........%s" % person.full_name
    print "first_name........%s" % person.first_name
    print "last_name.........%s" % person.last_name
    print "sex...............%s" % person.sex
    print "date_of_birth.....%s" % person.date_of_birth
    print "age...............%s" % person.age
    print "home_city.........%s" % person.home_city
    print "home_state........%s" % person.home_state
    print "home_neighborhood.%s" % person.home_neighborhood
    print "home_street.......%s" % person.home_street
    print "home_postal_code..%s" % person.home_postal_code
    print "photo_url.........%s" % person.photo_url
    print "other.............%s" % person.other
    print "home_country......%s" % person.home_country

def handle(message):
    data = urllib2.urlopen("%s%s" % (host, query_uri)).read()
    dom1 = dom.parseString(data)
    (persons, notes) = from_xml(dom1)
    found_persons = name_search(query, persons)
    persons_str = ""

    if found_persons:
        for person in found_persons:
            persons_str += format_info(person)

    return persons_str
