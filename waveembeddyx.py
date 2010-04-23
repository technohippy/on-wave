# -*- coding: utf-8 -*-

from waveapi import robot
from waveapi import events
from waveapi import element
import logging

GADGET_URL = 'http://waveembeddy.on-wave.appspot.com/embed_wave_gadget/%s'

class WaveEmbeddyX(robot.Robot):
  def __init__(self):
    robot.Robot.__init__(self, 'Wave Embeddy',
      image_url = 'http://on-wave.appspot.com/assets/waveembeddy_icon.png',
      profile_url = 'http://on-wave.appspot.com/'
    )
    self.register_handler(events.AnnotatedTextChanged, self.add_gadget, filter='link/wave')

  def add_gadget(self, events, wavelet):
    logging.info('ADD_GADGET')
    blip = events.blip
    if blip == None: return
    for annotation in blip.annotations:
      if annotation.name != 'link/wave': continue

      gadget_url = GADGET_URL % annotation.value

      has_gadget = False
      for other_blip_id in blip._other_blips:
        other_blip = blip._other_blips.get(other_blip_id)
        gadget = other_blip.first(element.Gadget, url=gadget_url)
        if gadget:
          has_gadget = True
          break
      if has_gadget: continue

      inline_blip = blip.insert_inline_blip(annotation.end)
      inline_blip.append(element.Gadget(url=gadget_url))
