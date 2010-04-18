# -*- coding: utf-8 -*-
from waveapi import robot
from waveapi import events
import appengine_multi_robot_runner

from waveembeddy import WaveEmbeddy

if __name__ == '__main__':
  appengine_multi_robot_runner.compound_and_run([
    ('waveembeddy', WaveEmbeddy())
  ])
