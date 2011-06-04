import xml.dom.minidom as dom

PFIF_12_NS = "http://zesty.ca/pfif/1.2"

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
    pfifdom = dom.getDOMImplementation().createDocument(PFIF_12_NS, "pfif", None)
    pfif = pfifdom.documentElement
    for person in persons:
        pfif.appendChild(person.to_xml(pfifdom))
    for note in notes:
        pfif.appendChild(note.to_xml(pfifdom))
    pfif.setAttribute("xmlns", PFIF_12_NS)
    pfif.setAttribute("xmlns:pfif", PFIF_12_NS)
    return pfif
    