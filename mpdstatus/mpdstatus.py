#!/usr/bin/env python

"""mpdstatus py3status module.

mpdstatus is a MPD module for py3status.
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

    def __init__(self, host, port, password, max_length):
        """Initialise MPD client."""
        self.HOST = host
        self.PORT = port
        self.PW = password
        self.MAX_LENGTH = max_length
        self.error = (None, None)
        self.client = MPDClient()
        self._connect()

    def _crop_text(self, text, length):
        """Crop string to specified length."""
        if not length:
            return text
        if len(text) > length:
            text = "{}...".format(text[:length])

        return text

    def _connect(self):
        """Connect to MPD."""
        try:
            self.client.connect(self.HOST, self.PORT)
            if self.PW:
                self.client.password(self.PW)
        except CommandError as e:
            if "incorrect password" in str(e).lower():
                raise MPDstatusException("incorrect password")
        except ConnectionRefusedError:
            # This is handled elsewhere by displaying the text `disconnected`
            pass

    def disconnect(self):
        """Close connection to MPD cleanly."""
        try:
            self.client.close()
            self.client.disconnect()
        except:
            # After long idle periods the client reaches a state where mpd2
            # is neither able to disconnect nor to reconnect anymore. Calling
            # `_reset` seems to remove the socket and make a new connection
            # attempt possible.
            self.client._reset()

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
        title = "Unknown Title"
        song = self.client.currentsong()
        status = self.client.status()
        length = self.MAX_LENGTH
        artist = self._crop_text(
            song['artist'], length) if 'artist' in song else "Unknown Artist"
        if 'title' in song:
            title = self._crop_text(song['title'], length)
        elif 'file' in song:
            title = self._crop_text(path.basename(song['file']), length)

        return artist, title, status.get('state', "unknown")


class Py3status:
    """This is where all the py3status magic happens."""

    cache_timeout = 0
    error_timeout = 10
    name = 'MPD:'
    host = 'localhost'
    port = 6600
    password = ''
    max_length = None
    hide_on_pause = False

    def __init__(self):
        """Initialisation."""
        self.data = None

    def _validate_config(self):
        """Validate configuration."""
        msg = []

        if type(self.name) != str:
            msg.append("invalid name")
        if type(self.port) != int or self.port < 1 or self.port > 65535:
            msg.append("invalid port")
        if type(self.max_length) != int or self.max_length < 1:
            msg.append("invalid max_length")

        if msg:
            self.data.error = ("configuration error: {}".format(
                ", ".join(msg)), -1)

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
        response = {'full_text': '', 'name': 'mpdstatus'}

        # Initialise Data class only once
        if not self.data:
            self.data = Data(self.host, self.port, self.password,
                             self.max_length)

        # Reset error message
        # -1 means we can't recover from this error
        if (self.data.error[0] and
                (self.data.error[1] + self.error_timeout < time() and
                    self.data.error[1] != -1)):
            self.data.error = (None, None)

        connection = self.data.has_connection()

        if connection:
            artist, songtitle, state = self.data.get_stats()

            response['full_text'] = "%s %s - %s" % \
                (self.name, artist, songtitle)

            if state == 'play':
                response['color'] = i3status_config['color_good']
            elif state == 'pause':
                response['color'] = i3status_config['color_degraded']
                if self.hide_on_pause is True:
                    response['full_text'] = self.name

        else:
            self.data.reconnect()
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s disconnected" % (self.name)

        response['cached_until'] = time() + self.cache_timeout

        return response


if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
    }
    while True:
        print(x.mpdstatus([], config))
        sleep(1)
