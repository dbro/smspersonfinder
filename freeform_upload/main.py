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
from django.utils import simplejson

import logging
import cgi
import datetime
import urllib
import wsgiref.handlers
from communication import upload_to_personfinder
import logging

class Message(db.Model):
    """Messages with status information"""
    status = db.StringProperty(choices=['NEW', 'UNPARSEABLE', 'SENT'])
    status_timestamp = db.DateTimeProperty(auto_now_add=True)
    source_phone_number = db.StringProperty()
    message_timestamp = db.DateTimeProperty(auto_now_add=True)
    message = db.StringProperty(multiline=True)
    parsed_message = db.StringProperty(multiline=True)

    def __str__(self):
        return "id=%s<br>status=%s<br>status_timestamp=%s<br>source=%s<br>message=%s<br>message_timestamp=%s" % (self.key(), self.status, self.status_timestamp, self.source_phone_number, self.message, self.message_timestamp)


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class CreateHandler(webapp.RequestHandler):
    def get(self):
        time = datetime.datetime.now()
        try:
            # TODO(amantri): Switch to post
            source = self.request.get('source')
            message = self.request.get('message')
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")
            return

        # try to upload to person finder, if it fails (i.e. has no #)
        try:
            logging.debug('trying to use formatted parsing method')
            upload_to_personfinder(time, source, message)
        except:
            logging.debug('falling back on crowdsource parsing method')
            self.create_task_for_crowdsource(time, source, message)

        self.response.out.write("<html><body><p>%s</p></body></html>" % message)

    def create_task_for_crowdsource(self, time, source, message):
        # TODO(amantri): set the key to be the hash of time, source and message to prevent dupes
        message = Message(message_timestamp=time,
            source_phone_number=source,
            message=message,
            status='NEW')
        message.put()

class PostHandler(webapp.RequestHandler):
    def get(self):
        self.fetch_task_for_crowdsource()

    def post(self):
        logging.debug('falling back on crowdsource parsing method')

    def fetch_task_for_crowdsource(self):
        # get the oldest new message
        q = Message.all()
        q.filter("status =", "NEW")
        q.order("status_timestamp")
        result = q.fetch(1)
        # TODO: deal with empty result set

        # update the status of the message with the current timestamp
        result.status_timestamp = datetime.datetime.now()
        result.put()

        # respond
        response = {
            'message':message,
            'timestamp':message_timestamp,
            'errorstatus':'ok',
            'id':message.key()
        }
        self.response.out.write(simplejson.dumps(response))

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/create', CreateHandler), 
        ('/post', PostHandler)], 
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
