import urllib2
import xml.dom.minidom as dom

PFIF_13_NS = "http://zesty.ca/pfif/1.3"

# As bizarre as it sounds, (mini)DOM doesn't provide a 
# getElementsByTag that gets from only the immediate children.
def get_qualified_xml_children(element, ns, name):
    elements = []
    for child in element.childNodes:
        if isinstance(child, dom.Element):
            if child.namespaceURI == ns and child.localName == name:
                elements.append(child)
    return elements

def add_string_element(dom, xmlnode, ns, name, data, attributes=()):
    if ns:
        e = dom.createElementNS(ns, name)
    else:
        e = dom.createElement(name)
    
    e.appendChild(dom.createTextNode(data))
    
    for (attr_name, attr_value) in attributes:
        e.setAttribute(attr_name, attr_value)
        
    xmlnode.appendChild(e)
    
def to_xml(persons=[], notes=[]):
    pfifdom = dom.getDOMImplementation().createDocument(PFIF_13_NS, "pfif", None)
    pfif = pfifdom.documentElement
    for person in persons:
        pfif.appendChild(person.to_xml(pfifdom))
    for note in notes:
        pfif.appendChild(note.to_xml(pfifdom))
    pfif.setAttribute("xmlns", PFIF_13_NS)
    pfif.setAttribute("xmlns:pfif", PFIF_13_NS)
    return pfif

def from_xml_str(pfif_string):
    return from_xml(dom.parseString(pfif_string))
    
def from_xml(dom):
    persons = []
    notes = []
    
    pfif = dom.documentElement
    personsxml = get_qualified_xml_children(pfif, PFIF_13_NS, "person")
    for personxml in personsxml:
        persons.append(Person.from_xml(personxml))
    
    notesxml = get_qualified_xml_children(pfif, PFIF_13_NS, "note")
    for notexml in notesxml:
        notes.append(Note.from_xml(notexml))
    
    return (persons, notes)

PFIF_13_PERSON_ATTRS = (
    "person_record_id",
    "entry_date",
    "expiry_date",
    "author_name",
    "author_email",
    "author_phone",
    "source_name",
    "source_date",
    "source_url",
    "full_name",
    "first_name",
    "last_name",
    "sex",
    "date_of_birth",
    "age",
    "home_city",
    "home_state",
    "home_neighborhood",
    "home_street",
    "home_postal_code",
    "photo_url",
    "other",
    "home_country",
)

PFIF_13_NOTE_ATTRS = (
    "note_record_id",
    "person_record_id",
    "linked_person_record_id",
    "entry_date",
    "author_name",
    "author_email",
    "author_phone",
    "source_date",
    "found",
    "email_of_found_person",
    "phone_of_found_person",
    "last_known_location",
    "text",
    "status",
)

class Person:
    def __init__(self, *args, **kwargs):
        for attr in PFIF_13_PERSON_ATTRS:
            setattr(self, attr, kwargs.get(attr, None))
        self.notes = kwargs.get("notes", [])

    def add_note(self, note):
        self.notes.append(note)
        
    def to_xml(self, dom):
        # TODO: Return error codes instead?
        assert self.person_record_id is not None and \
               self.first_name is not None and \
               self.last_name is not None

        pxml = dom.createElementNS(PFIF_13_NS, "person")
        for attr in PFIF_13_PERSON_ATTRS:
            if getattr(self, attr) is not None:
                add_string_element(dom, pxml, PFIF_13_NS, attr, getattr(self, attr))
        
        for note in self.notes:
            pxml.appendChild(note.to_xml(dom))
            
        return pxml
    
    @classmethod
    def from_xml(cls, personxml):
        person = Person()
        for e in personxml.getElementsByTagName("*"):
            if e.localName == "note":
                person.add_note(Note.from_xml(e))
                continue
            
            if e.firstChild is not None:
                setattr(person, e.localName, e.firstChild.data.strip())
        return person
    
class Note:
    def __init__(self, *args, **kwargs):
        for attr in PFIF_13_NOTE_ATTRS:
            setattr(self, attr, kwargs.get(attr, None))

    def to_xml(self, dom):
        # TODO: Return error codes instead?
        assert self.note_record_id is not None and \
               self.author_name is not None

        pxml = dom.createElementNS(PFIF_13_NS, "note")
        for attr in PFIF_13_NOTE_ATTRS:
            if getattr(self, attr) is not None:
                add_string_element(dom, pxml, PFIF_13_NS, attr, getattr(self, attr))
        
        return pxml
    
    @classmethod
    def from_xml(cls, notexml):
        note = Note()
        for e in notexml.getElementsByTagName("*"):
            if e.firstChild is not None:
                setattr(note, e.localName, e.firstChild.data.strip())
        return note
        
def build_search_url(key, domain, query):
    """
    Action is write/note/person
    """
    url = "http://googlepersonfinder.appspot.com/api/search?key=%s&subdomain=%s&q=%s" % (key, domain, query)
    return url

domain = "rhok"
key = ""
action = "search"
query = currentCall.initialText
found = 0

url = build_search_url(key, domain, query)
req = urllib2.Request(url, None)
data = urllib2.urlopen(req).read()

dom1 = dom.parseString(data)
(persons, notes) = from_xml(dom1)

for person in persons:
    if found == 1:
        break
    elif person.first_name == query :
        found_person = person
        found = 1

if found == 1 :
    say("we found %s %s" % (found_person.first_name, found_person.last_name))
else :
    say("we did not find %s" % query)