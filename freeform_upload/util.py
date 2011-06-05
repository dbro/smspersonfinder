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
    from models import Person, Note
    
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
