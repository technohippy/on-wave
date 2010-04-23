# -*- coding: utf-8 -*-

from waveapi import robot
from waveapi import events
from waveapi import element
import logging

BUTTON_GADGET_URL = 'http://waveembeddy.on-wave.appspot.com/embed_wave_button_gadget'
GADGET_URL = 'http://waveembeddy.on-wave.appspot.com/embed_wave_gadget/%s'

class WaveEmbeddy(robot.Robot):
  def __init__(self):
    robot.Robot.__init__(self, 'Wave Embeddy', 
      image_url = 'http://on-wave.appspot.com/assets/waveembeddy_icon.png', 
      profile_url = 'http://on-wave.appspot.com/'
    )
    self.register_handler(events.AnnotatedTextChanged, self.on_annotated_text_changed)
    self.register_handler(events.GadgetStateChanged, self.convert_gadget)

  def on_annotated_text_changed(self, events, wavelet):
    if events.name == 'link/wave':
      self.add_button_gadget(events, wavelet)
    elif events.name == 'force_embed_wave':
      self.add_gadget_for_selection(events, wavelet)

  def add_gadget_for_selection(self, events, wavelet):
    blip = events.blip
    selection = None
    for annotation in blip.annotations:
      if annotation.name == 'force_embed_wave':
        selection = annotation
        break
    if selection:
      for annotation in blip.annotations:
        if annotation.name == 'link/wave':
          if (annotation.start <= selection.start <= annotation.end) or (annotation.start <= selection.start <= annotation.end):
            wave_id = annotation.value
            gadget_url = GADGET_URL % wave_id
            inline_blip = blip.insert_inline_blip(annotation.end)
            inline_blip.append(element.Gadget(url=gadget_url))
      selection_ref = blip.range(selection.start, selection.end)
      selection_ref.clear_annotation('force_embed_wave')

  def lap_over_annotation(self, blip, link_wave_annotation):
    for annotation in blip.annotations:
      logging.info(annotation.serialize())
      if annotation.start == link_wave_annotation.start and annotation.start == link_wave_annotation.start and annotation.name == 'embed_wave':
        return annotation
    return None

  def add_button_gadget(self, events, wavelet):
    blip = events.blip
    if blip == None: return
    for annotation in blip.annotations:
      if annotation.name != 'link/wave': continue

      embed_wave_annotation = self.lap_over_annotation(blip, annotation)
      if embed_wave_annotation:
        if embed_wave_annotation.get('embed_wave') == 'no':
          return

      wave_id = annotation.value

      button_gadget_url = BUTTON_GADGET_URL
      gadget_url = GADGET_URL % wave_id
      
      has_button_gadget = False
      gadget_refs = blip.all(element.Gadget, url=BUTTON_GADGET_URL)
      for start_end in gadget_refs:
        gadget_ref = blip.range(start_end[0], start_end[1])
        if wave_id == gadget_ref.value().get('wave_id'):
          has_button_gadget = True
          break
      if has_button_gadget: continue

      has_gadget = False
      for other_blip_id in blip._other_blips:
        other_blip = blip._other_blips.get(other_blip_id)
        gadget = other_blip.first(element.Gadget, url=gadget_url)
        if gadget:
          has_gadget = True
          break
      if has_gadget: continue

      blip_ref = blip.range(annotation.start, annotation.end)
      blip_ref.insert_after(element.Gadget(url=button_gadget_url, props={'wave_id':wave_id}))

  def target_wavelink(self, events, wavelet):
    index = events.index - 1
    blip = events.blip
    for annotation in blip.annotations:
      if annotation.start <= index <= annotation.end:
        return annotation
    return None

  def convert_gadget(self, events, wavelet):
    blip = events.blip
    button_gadget_ref = blip.at(events.index)
    button_gadget = button_gadget_ref.value()
    type = button_gadget.get('function', 'convert')
    if type == 'remove':
      wavelink = self.target_wavelink(events, wavelet)
      if wavelink:
        blip_ref = blip.range(wavelink.start, wavelink.end)
        blip_ref.annotate('embed_wave', 'no')
      button_gadget_ref.delete()
    elif type == 'convert':
      wave_id = button_gadget.get('wave_id')
      logging.info('waveid: ' + wave_id)

      gadget_url = GADGET_URL % wave_id
      #button_gadget_ref.replace(element.Gadget(url=gadget_url))
      button_gadget_ref.delete()
      inline_blip = blip.insert_inline_blip(events.index)
      inline_blip.append(element.Gadget(url=gadget_url))
