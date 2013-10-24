#!/usr/bin/env python

"""mpdstatus

Mpdstatus is a MPD module for py3status.
It shows the currently playing song and can be used to pause, resume or stop
playpack.

Copyright (C) 2013 Tablet Mode <tablet-mode AT monochromatic DOT cc>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/].
"""

from configparser import SafeConfigParser, NoSectionError, NoOptionError
from mpd import MPDClient
from os import path
from shlex import split
from sys import stderr
from time import time

class _Data:
    """Aquire data."""

    def read_config(self):
        """Read config file.
        Exit on invalid config.
        """
        config = SafeConfigParser({'title': 'MPD:', 'order': '0',
            'interval': '0', 'host': 'localhost', 'port': '6600'})
        config.read([path.expanduser('~/.i3/py3status/modules.cfg')])
        try:
            self.TITLE = split(config.get('mpdstatus', 'title'))[0]
            self.ORDER = config.getint('mpdstatus', 'order')
            self.INTERVAL = config.getint('mpdstatus', 'interval')
            self.HOST = split(config.get('mpdstatus', 'host'))[0]
            self.PORT = config.getint('mpdstatus', 'port')
        except NoSectionError:
            stderr.write("\nmpdstatus: no mpdstatus section in config.\n\n")
            self.TITLE = split(config.get('DEFAULT', 'title'))[0]
            self.ORDER = config.getint('DEFAULT', 'order')
            self.INTERVAL = config.getint('DEFAULT', 'interval')
            self.HOST = split(config.get('DEFAULT', 'host'))[0]
            self.PORT = config.getint('DEFAULT', 'port')

    def connect(self):
        """Connect to MPD Server."""
        self.client = MPDClient()
        try:
            self.client.connect(self.HOST, self.PORT)
        except:
            stderr.write("\nmpdstatus: couldn't connect to mpd.\n\n")
            return False
        else:
            return True

    def previous(self):
        self.client.previous()

    def next(self):
        self.client.next()

    def pause(self):
        self.client.pause()

    def get_stats(self):
        """Return Artist, Songtitle and Playback State."""
        song = self.client.currentsong()
        status = self.client.status()

        artist = song['artist']

        return artist, song['title'], status['state']


class Py3status:

    def __init__(self):
        self.data = _Data()
        self.data.read_config()
        self.connection = self.data.connect()

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        if event['button'] == 1:
            self.data.previous()
        elif event['button'] == 2:
            self.data.pause()
        elif event['button'] == 3:
            self.data.next()

    def mpdstatus(self, json, i3status_config):
        response = {'full_text': '', 'name': 'mpdstatus'}
        
        if self.connection:
            artist, title, state = self.data.get_stats()

            if state == 'play':
                response['color'] = i3status_config['color_good']
            elif state == 'pause':
                response['color'] = i3status_config['color_degraded']

            response['full_text'] = "%s %s - %s" % \
                    (self.data.TITLE, artist, title)
        else:
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s not connected" % (self.data.TITLE)

        response['cached_until'] = time() + self.data.INTERVAL

        return (self.data.ORDER, response)
