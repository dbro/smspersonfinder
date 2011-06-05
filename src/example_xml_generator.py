#!/usr/bin/env python
from models import *
from util import *
p = Person()
p.person_record_id = "rhok1.com/person.90976"
p.entry_date = "2011-06-03T18:49:47Z"
p.expiry_date = "2011-07-01T18:49:47Z"
p.author_name = "Test Doe"
p.first_name = "Test"
p.last_name = "Doe"


n = Note()
n.note_record_id = "rhok1.com/note.909761"
n.author_name = "Test Doe"
n.text = "This is sample note."
n.source_date = "2011-06-03T18:49:47Z"

p.add_note(n)

#print to_xml(persons=[p]).toprettyxml()
print to_xml(persons=[p]).toxml()
 
