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

from configparser import SafeConfigParser, NoSectionError
from os import path
from time import time

from mpd import MPDClient, CommandError


class MPDstatusException(Exception):

    """Custom mpdstatus exception."""

    def __init__(self, exception):
        """Initialisation."""
        self.exception = exception

    def __str__(self):
        """Prepend message with 'mpdstatus: '."""
        return "mpdstatus: {exception}".format(exception=self.exception)


class Data:

    """Aquire data."""

    def __init__(self, host, port, password):
        """Initialise MPD client."""
        self.count = 0
        self.HOST = host
        self.PORT = port
        self.PW = password
        self.client = MPDClient()
        self._connect()

    def _connect(self):
        """Connect to MPD."""
        try:
            self.client.connect(self.HOST, self.PORT)
            if self.PW:
                self.client.password(self.PW)
        except CommandError as e:
            if "incorrect password" in str(e).lower():
                raise MPDstatusException("incorrect password")

    def disconnect(self):
        """Close connection to MPD cleanly."""
        try:
            self.client.close()
            self.client.disconnect()
        except:
            # If this happens,  the client is most likely already disconnected
            # anyway.
            pass

    def reconnect(self):
        """Try to reaquire MPD connection."""
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
        """Jump to previous song."""
        self.client.previous()

    def next(self):
        """Go to next song."""
        self.client.next()

    def pause(self):
        """Pause playback."""
        self.client.pause()

    def get_stats(self):
        """Return artist, songtitle and playback state."""
        song = self.client.currentsong()
        status = self.client.status()
        artist = song['artist']

        return artist, song['title'], status['state']


class Py3status:

    """This is where all the py3status magic happens."""

    def __init__(self):
        """Read config and initialise Data class."""
        self.conf = self._read_config()
        self.data = Data(
            self.conf['host'], self.conf['port'], self.conf['password'])

    def _read_config(self):
        """Read config file."""
        conf = {}
        config = SafeConfigParser({
            'title': 'MPD:', 'order': '0', 'interval': '0',
            'host': 'localhost', 'port': '6600', 'password': None})
        config.read([path.expanduser('~/.i3/py3status/modules.ini')])
        try:
            conf['title'] = config.get('mpdstatus', 'title')
            conf['order'] = config.getint('mpdstatus', 'order')
            conf['interval'] = config.getint('mpdstatus', 'interval')
            conf['host'] = config.get('mpdstatus', 'host')
            conf['port'] = config.getint('mpdstatus', 'port')
            conf['password'] = config.get('mpdstatus', 'password')
        except NoSectionError:
            # Fallback settings in case there is no mpdstatus configuration.
            conf['title'] = config.get('DEFAULT', 'title')
            conf['order'] = config.getint('DEFAULT', 'order')
            conf['interval'] = config.getint('DEFAULT', 'interval')
            conf['host'] = config.get('DEFAULT', 'host')
            conf['port'] = config.getint('DEFAULT', 'port')
            conf['password'] = config.get('DEFAULT', 'password')

        return conf

    def kill(self, json, i3status_config, event):
        """Handle termination."""
        self.data.disconnect()

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        # Left click: Go to previous song
        if event['button'] == 1:
            self.data.previous()
        # Middle click: Pause playback
        elif event['button'] == 2:
            self.data.pause()
        # Right click: Jump to next song
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
