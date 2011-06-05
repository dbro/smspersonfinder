#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext import db

import cgi
import datetime
import urllib
import wsgiref.handlers


class Message(db.Model):
  """Messages with status information"""
  status = db.StringProperty(choices=['NEW', 'UNPARSEABLE', 'SENT'])
  status_timestamp = db.DateTimeProperty(auto_now_add=True)
  source_phone_number = db.StringProperty()
  message_timestamp = db.StringProperty()
  message = db.StringProperty(multiline=True)
  parsed_message = db.StringProperty(multiline=True)

  def __str__(self):
    return "id=%s<br>status=%s<br>status_timestamp=%s<br>source=%s<br>message=%s<br>message_timestamp=%s" % (self.key(), self.status, self.status_timestamp, self.source_phone_number, self.message, self.message_timestamp)


class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write('Hello world!')

class CreateHandler(webapp.RequestHandler):
  def get(self):
    try:
      # TODO(amantri): Switch to post
      time = self.request.get('time')
      source = self.request.get('source')
      message = self.request.get('message')

      # TODO(amantri): set the key to be the has of time, source and message to prevent dupes
      message = Message(message_timestamp=time,
                    source_phone_number=source,
                    message=message,
                    status='NEW')
      message.put()

      self.response.out.write("<html><body><p>%s</p></body></html>" %
          message)
    except (TypeError, ValueError):
      self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/create', CreateHandler)], 
                                         debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()