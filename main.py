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

import cgi
import datetime
import urllib
import wsgiref.handlers
import logging
import search 
import models
import uuid
from communication import parse_formatted_message, upload_to_personfinder, split_message_to_fields

class Message(db.Model):
    """Messages with status information"""
    status = db.StringProperty(choices=['NEW', 'UNPARSEABLE', 'SENT'])
    status_timestamp = db.DateTimeProperty(auto_now_add=True)
    source_phone_number = db.StringProperty()
    message_timestamp = db.DateTimeProperty(auto_now_add=True)
    message = db.StringProperty(multiline=True)
    parsed_message = db.StringProperty(multiline=True)

    def __str__(self):
        return "id=%s<br>status=%s<br>status_timestamp=%s<br>source=%s<br>message=%s<br>message_timestamp=%s" % (self.key().id(), self.status, self.status_timestamp, self.source_phone_number, self.message, self.message_timestamp)

class Accumulator(db.Model):
  name = db.StringProperty()
  counter = db.IntegerProperty()

def atomic_add_to_counter(ctr_name, val):
  def add_to_counter(key, val):
    obj = db.get(key)
    obj.counter += val
    obj.put()

  q = db.GqlQuery("SELECT * FROM Accumulator WHERE name = :1", ctr_name)
  acc = q.get()
  if acc == None:
    acc = Accumulator()
    acc.name = ctr_name
    acc.counter = val
    acc.put()
  else:
    db.run_in_transaction(add_to_counter, acc.key(), val)

def get_counter(ctr_name):
  q = db.GqlQuery("SELECT * FROM Accumulator WHERE name = :1", ctr_name)
  acc = q.get()
  return acc.counter

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write('SMS person finder')

class CreateHandler(webapp.RequestHandler):
    def get(self):
        try:
            # TODO(amantri): Switch to post
            source = self.request.get('source')
            message = self.request.get('message')
            time = self.request.get('time')
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")
            return

        # try to upload to person finder, if it fails (i.e. has no #)
        try:
            logging.debug('trying to use formatted parsing method')
            person = parse_formatted_message(time, source, message)
            upload_to_personfinder(person)

            fields = split_message_to_fields(message)
            reply = 'Added to Person Finder.\nName: %s %s' % (fields['person_first_name'],
                                                               fields['person_last_name'])
            # limit to 140
            reply = reply[0:139]
        except:
            logging.debug('falling back on crowdsource parsing method')
            message = self.create_task_for_crowdsource(time, source, message)
            message.put()
            reply = "Sent to crowd-source for input. For instant upload to Person Finder, use the format last_name#first_name#status_of_person#description"

        self.response.out.write("%s" % reply)

    def create_task_for_crowdsource(self, timestr, source, message):
        # TODO(amantri): set the key to be the hash of time, source and message to prevent dupes
        dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        message = Message(message_timestamp=dt,
            source_phone_number=source,
            message=message,
            status='NEW')
        return message


class PostHandler(webapp.RequestHandler):
    #Added by Dan for testing
    def get(self):
        self.post()

    def post(self):
        logging.debug('post handler post method called')
        errorresult = False
        if self.request.get('id'):
            errorresult = self.update_parsed_message()
        self.fetch_task_for_crowdsource(errorresult)

    def fetch_task_for_crowdsource(self, errorfromlastpost = False):
        logging.debug('fetch task for crowdsource method called')
        # get the oldest new message
        q = Message.all()
        q.filter("status =", "NEW")
        q.order("status_timestamp")
        results = q.fetch(1)
        logging.debug('results from database: %s' % repr(results))

        # update the status of the message with the current timestamp
        response = {}
        if len(results):
            r = results[0]
            response = {
                'message' : r.message,
                'timestamp' : datetime.datetime.isoformat(r.message_timestamp, ' '),
                'errorstatus' : 'parse_error' if errorfromlastpost else 'ok',
                'id' : repr(r.key().id())
            }
            r.status_timestamp = datetime.datetime.now()
            r.put()
        else:
            # TODO: properly deal with empty result set
            logging.debug('no messages available for human parsing')

        # respond
        self.response.out.write(simplejson.dumps(response))
    
    def update_parsed_message(self):
        logging.debug('update parsed message method called')
        logging.debug('Request: %s' % self.request)
        message = Message.get_by_id(long(self.request.get('id')))

        p = models.Person()
        namespace = "rhok1.com"
        unique_id = uuid.uuid1()
        p.person_record_id = '%s/person.%s' % (namespace, unique_id)
        p.author_name = message.source_phone_number

        for attr in models.PFIF_13_PERSON_ATTRS:
            if self.request.get(attr):
                logging.debug('%s: %s' % (attr, self.request.get(attr)))
                setattr(p, attr, self.request.get(attr))

        for attr in models.PFIF_13_NOTE_ATTRS:
            if self.request.get(attr):
                if not p.notes:
                    n = models.Note()
                    n.note_record_id = '%s/note.%s' % (namespace, unique_id)
                    n.author_name = message.source_phone_number
                    p.notes.append(n)
                setattr(p.notes[0], attr, self.request.get(attr))

        logging.debug('###### Here')
        message.status_timestamp = datetime.datetime.now()
        errorparsing = False
        if self.request.get('parseable').lower() == 'false':
            message.status = 'UNPARSEABLE'
            errorparsing = True
        else:
            upload_to_personfinder(p)
            message.status = 'SENT'

        logging.debug('Person: %s' % repr(p))
        logging.debug('Message: %s' % message)
        message.put()
        return errorparsing

class SearchHandler(webapp.RequestHandler):
    def get(self):
        try:
            message = self.request.get('message')
        except (TypeError, ValueError):
            self.response.set_status(400);
            self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")
            return
        
        result = search.handle(message)
        self.response.out.write(result)
        return

    def post(self):
        self.response.set_status(405);
        self.response.out.write("POST not supported")

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/create', CreateHandler), 
        ('/post', PostHandler),
        ('/search', SearchHandler)],
        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
