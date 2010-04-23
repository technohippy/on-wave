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
from google.appengine.ext.webapp import template
import os


class MainHandler(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, { }))


def EmbedGadgetWithEncodedWaveId(handler, encoded_wave_id, gadget_filename):
  wave_id = encoded_wave_id.replace('%21', '!').replace('%2B', '+')
  wave_server = 'http://wave.google.com/'
  if wave_id.find('wavesandbox') < 0:
    wave_server = wave_server + 'wave/'
  else:
    wave_server = wave_server + 'a/wavesandbox.com/'
  path = os.path.join(os.path.dirname(__file__), gadget_filename)
  handler.response.out.write(template.render(path, {
    'encoded_wave_id': encoded_wave_id,
    'wave_id': wave_id,
    'wave_server': wave_server
  }))

class EmbedWaveButtonGadgetHandler(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'embed_wave_button_gadget.xml')
    self.response.out.write(template.render(path, { }))

class EmbedWaveGadgetHandler(webapp.RequestHandler):
  def get(self, encoded_wave_id):
    wave_id = encoded_wave_id.replace('%21', '!').replace('%2B', '+')
    wave_server = 'http://wave.google.com/'
    if wave_id.find('wavesandbox') < 0:
      wave_server = wave_server + 'wave/'
    else:
      wave_server = wave_server + 'a/wavesandbox.com/'
    path = os.path.join(os.path.dirname(__file__), 'embed_wave_gadget.xml')
    self.response.out.write(template.render(path, {
      'wave_id': wave_id,
      'wave_server': wave_server
    }))

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/embed_wave_button_gadget', EmbedWaveButtonGadgetHandler),
                                        ('/embed_wave_gadget/(.*)', EmbedWaveGadgetHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
