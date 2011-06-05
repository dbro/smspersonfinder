from util import add_string_element

PFIF_13_NS = "http://zesty.ca/pfif/1.3"

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
        
    