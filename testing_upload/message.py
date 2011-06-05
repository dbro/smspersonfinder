class FormattedMessage:
  """A Google Person Finder report"""
  def __init__(self, namespace, fmtd_msg):
    self.namespace = namespace

    # Formatted message format: Last#First#Comment
    fields = fmtd_msg.split('#')
    self.person_info = {}
    self.person_info['last_name'] = fields[0]
    self.person_info['first_name'] = fields[1]
    self.person_info['comments'] = fields[2]

  def serializeAsPFIF(self):
    return """<?xml version="1.0" encoding="UTF-8"?> 
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
      'first_name': self.person_info.get('first_name', ''),
      'last_name': self.person_info.get('last_name', ''),
      'comments': self.person_info.get('comments', 'No information'),
      'namespace': self.namespace
    }
