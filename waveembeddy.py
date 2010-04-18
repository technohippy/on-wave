# -*- coding: utf-8 -*-

from waveapi import robot
from waveapi import events
from waveapi import element
import logging

GADGET_URL = 'http://waveembeddy.on-wave.appspot.com/embed_wave_gadget/%s'

class WaveEmbeddy(robot.Robot):
  def __init__(self):
    robot.Robot.__init__(self, 'Wave Embeddy',
      image_url = 'http://on-wave.appspot.com/assets/waveembeddy_icon.png'
    )
    self.register_handler(events.AnnotatedTextChanged, self.add_gadget, filter='link/wave')

  def add_gadget(self, events, wavelet):
    logging.info('ADD_GADGET')
    blip = events.blip
    if blip == None: return
    for annotation in blip.annotations:
      if annotation.name != 'link/wave': continue

      gadget_url = GADGET_URL % annotation.value
      gadget = blip.first(element.Gadget, url=gadget_url)
      if gadget: continue

      blip_ref = blip.range(annotation.start, annotation.end)
      blip_ref.insert_after(element.Gadget(url=gadget_url))
