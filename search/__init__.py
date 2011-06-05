import urllib2
from models import *
from util import *
import urllib

SubDomain = "rhok"
AuthToken = "soNQ67BhLRP0tIvP"
host = "https://googlepersonfinder.appspot.com"

SMS_MAXLEN = 140
SMS_RESULT_MAXLEN = SMS_MAXLEN*2
SMS_FIELD_SEP = "/"
SMS_PERSON_SEP = "##"

def chop(str, length):
    if len(str) > length:
        str = str[0:length-3] + "..."
    return str

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

def format_name(person):
    SMS_NAME_SEP = ","
    
    name = ""
    if person.full_name:
        name = person.full_name.split("\n")[0]
    else:
        if person.last_name:
            name += person.last_name
        if person.first_name:
            if name:
                name += SMS_NAME_SEP
            name += person.first_name
    return name

def format_home_address(person):
    SMS_ADDRESS_SEP = ","
    
    if person.home_postal_code:
        return person.home_postal_code
    
    address = ""
    if person.home_street:
        address += person.home_street
    elif person.home_neighborhood:
        if address:
            address += SMS_ADDRESS_SEP
        address += person.home_neighborhood 
    
    if person.home_city:
        if address:
            address += SMS_ADDRESS_SEP
        address += person.home_city
    if person.home_state:
        if address:
            address += SMS_ADDRESS_SEP
        address += person.home_state
    
    # GFR: I think country is probably useless since there's one app per country.
    return address

def format_info(person) :
    result=""
    
    result += format_name(person) + SMS_FIELD_SEP
    
    if person.sex:
        result += person.sex + SMS_FIELD_SEP
    
    if person.date_of_birth:
        result += person.date_of_birth + SMS_FIELD_SEP
    elif person.age:
        result += person.age + SMS_FIELD_SEP

    result += format_home_address(person) + SMS_FIELD_SEP
    
    # person.other might have the description of the person
    result += chop(person.other, 10)
     
    person.found_status = None
    person.found_location = None
    person.found_contact = None
    person.found_text = None

    while len(person.notes):
        note = person.notes.pop()
        if not person.found_status and note.status:
            if note.status == 'is_note_author':
                note.status = 'believed_alive'
            person.found_status = note.status
            #Collect Note text from the last known status
            # GFR: this text can be big, we should find the sweet spot to chop
            if note.text:
                person.found_text = chop(note.text, 10)
        if not person.found_location and note.last_known_location:
            person.found_location = note.last_known_location
        if not person.found_contact and note.phone_of_found_person:
            person.found_contact = note.phone_of_found_person
        
        if person.found_status and person.found_location and person.found_contact:
            break

    if not person.found_status:
        found_status = "no_status"
    
    result += found_status + SMS_FIELD_SEP
    if person.found_contact:
        result += person.found_contact + SMS_FIELD_SEP
    if person.found_location:
        result += person.found_location + SMS_FIELD_SEP
    if person.found_text:
        result += person.found_text
    
    #print result
    return result

def print_person_info(person):
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

def print_note_info(note):
    print "note_record_id..............%s" % note.note_record_id
    print "person_record_id............%s" % note.person_record_id
    print "linked_person_record_id.....%s" % note.linked_person_record_id
    print "entry_date..................%s" % note.entry_date
    print "author_name.................%s" % note.author_name
    print "author_email................%s" % note.author_email
    print "author_phone................%s" % note.author_phone
    print "source_date.................%s" % note.source_date
    print "found.......................%s" % note.found
    print "email_of_found_person.......%s" % note.email_of_found_person
    print "phone_of_found_person.......%s" % note.phone_of_found_person
    print "last_known_location.........%s" % note.last_known_location
    print "text........................%s" % note.text
    print "status......................%s" % note.status

def compact_format_info(persons):
    return ""

def get_refinement_criteria(persons):
    SMS_ATTR_SEP = "#"
    
    response = "Too many hits, refine (ex. name#age=9#sex=M): "
    attrs = hot_attrs(persons)
    for (attr, count, values) in attrs:
        if count == 1:
            break
        response += SMS_ATTR_SEP + attr + "=["
        attr_values = ""
        for v in values:
            if attr_values:
                attr_values += ","
            attr_values += v
        response += "]"
        
    chop(response, SMS_RESULT_MAXLEN)
    return response

def handle(message):
    query_uri = "/api/search?key=" + AuthToken + "&subdomain=" + SubDomain + "&q=" + message
    data = urllib2.urlopen("%s%s" % (host, query_uri)).read()
    dom1 = dom.parseString(data)
    (persons, notes) = from_xml(dom1)
    #found_persons = name_search(message, persons)
    if not persons:
        return chop("No results found for: %s" % urllib.unquote(message), SMS_MAXLEN)
    
    persons_str = ""
    for person in persons:
        #add a new line after each person entry in the result
        if persons_str:
            persons_str += SMS_PERSON_SEP
        persons_str += format_info(person)

    if persons_str > SMS_RESULT_MAXLEN:
        persons_str = compact_format_info(persons)
        
        if persons_str > SMS_RESULT_MAXLEN:
            return get_refinement_criteria(persons)
            
    return persons_str
