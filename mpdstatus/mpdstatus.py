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

# TODO: allow configuration of multiple mpd connections.

from configparser import SafeConfigParser, NoSectionError
from os import path
from shlex import split
from time import time

from mpd import MPDClient


class Data:
    """Aquire data."""

    def __init__(self, host, port):
        self.count = 0
        self.HOST = host
        self.HOST = "10.0.0.2"
        self.PORT = port
        self.client = MPDClient()
        self._connect()

    def _connect(self):
        """Connect to MPD."""
        try:
            self.client.connect(self.HOST, self.PORT)
        except:
            raise Exception(
                "mpdstatus: couldn't connect to %s at port %d" %
                (self.HOST, self.PORT))

    def disconnect(self):
        """Close connection to MPD cleanly."""
        try:
            self.client.close()
            self.client.disconnect()
        except:
            pass

    def reconnect(self):
        self.disconnect()
        self._connect()

    def has_connection(self):
        """Check if MPD is reachable."""
        try:
            self.client.status()
        except:
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
        self.conf = self._read_config()
        self.data = Data(self.conf['host'], self.conf['port'])

    def _read_config(self):
        """Read config file."""
        conf = {}
        config = SafeConfigParser({
            'title': 'MPD:', 'order': '0', 'interval': '0',
            'host': 'localhost', 'port': '6600'})
        config.read([path.expanduser('~/.i3/py3status/modules.ini')])
        try:
            conf['title'] = split(config.get('mpdstatus', 'title'))[0]
            conf['order'] = config.getint('mpdstatus', 'order')
            conf['interval'] = config.getint('mpdstatus', 'interval')
            conf['host'] = split(config.get('mpdstatus', 'host'))[0]
            conf['port'] = config.getint('mpdstatus', 'port')
        except NoSectionError:
            raise Exception("mpdstatus: no mpdstatus section in config")
            conf['title'] = split(config.get('DEFAULT', 'title'))[0]
            conf['order'] = config.getint('DEFAULT', 'order')
            conf['interval'] = config.getint('DEFAULT', 'interval')
            conf['host'] = split(config.get('DEFAULT', 'host'))[0]
            conf['port'] = config.getint('DEFAULT', 'port')

        return conf

    def kill(self, json, i3status_config, event):
        """Handle termination."""
        self.data.disconnect()

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        if event['button'] == 1:
            self.data.previous()
        elif event['button'] == 2:
            self.data.pause()
        elif event['button'] == 3:
            self.data.next()

    def mpdstatus(self, json, i3status_config):
        """Return response for i3status bar."""
        TITLE = self.conf['title']
        INTERVAL = self.conf['interval']
        ORDER = self.conf['order']
        response = {'full_text': '', 'name': 'mpdstatus'}
        connection = self.data.has_connection()

        if connection:
            artist, songtitle, state = self.data.get_stats()

            if state == 'play':
                response['color'] = i3status_config['color_good']
            elif state == 'pause':
                response['color'] = i3status_config['color_degraded']

            response['full_text'] = "%s %s - %s" % \
                (TITLE, artist, songtitle)
        else:
            self.data.reconnect()
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s not connected" % (TITLE)

        response['cached_until'] = time() + INTERVAL

        return (ORDER, response)
