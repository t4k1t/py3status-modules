#!/usr/bin/env python

"""alsastatus py3status module.

alsastatus is an ALSA module for py3status.

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

from subprocess import check_output, CalledProcessError, STDOUT
from time import time


class Data:

    """Aquire data."""

    def __init__(self, mixer='Master'):
        """Initialise ALSA stuff."""
        self.volume = "-"
        self.mute = False
        self.mixer = mixer

    def decrease_volume(self, step=3):
        """Decrease volume."""
        check_output(
            ["amixer", "-q", "sset", self.mixer, "{}-".format(step)],
            stderr=STDOUT)

    def increase_volume(self, step=3):
        """Increase volume."""
        check_output(
            ["amixer", "-q", "sset", self.mixer, "{}+".format(step)],
            stderr=STDOUT)

    def toggle_mute(self):
        """Toggle mute."""
        out = check_output(
            ["amixer", "get", self.mixer], stderr=STDOUT).splitlines()
        mute = out[-1].split()[5].strip(b'[]').decode('utf-8')  # whut?

        if mute == "on":
            check_output(
                ["amixer", "-q", "sset", self.mixer, "mute"],
                stderr=STDOUT)
            self.mute = True
        else:
            check_output(
                ["amixer", "-q", "sset", self.mixer, "unmute"],
                stderr=STDOUT)
            self.mute = False

    def get_stats(self):
        """Return volume and mute status."""
        out = check_output(
            ["amixer", "get", self.mixer], stderr=STDOUT).splitlines()

        self.volume = out[-1].split()[3].strip(b'[]').decode('utf-8')  # whut?

        mute_str = out[-1].split()[5].strip(b'[]').decode('utf-8')  # whut?
        self.mute = True if mute_str == "off" else False

        return self.volume, self.mute


class Py3status:

    """This is where all the py3status magic happens."""

    cache_timeout = 0
    name = 'ALSA:'
    mixer = 'Master'
    indicator = '[M]'

    def __init__(self):
        """Read config and initialise Data class."""
        self.data = None

    def kill(self, json, i3status_config, event):
        """Handle termination."""
        pass

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        # Left click: Decrease volume
        if event['button'] == 1:
            self.data.decrease_volume()

        # Middle click: Mute/Unmute
        elif event['button'] == 2:
            self.data.toggle_mute()

        # Right click: Increase volume
        elif event['button'] == 3:
            self.data.increase_volume()

    def alsastatus(self, json, i3status_config):
        """Return response for i3status bar."""
        # Initialise Data class only once
        # TODO: parse settings in separate function for better error handling
        if not self.data:
            self.data = Data()

        volume, mute = self.data.get_stats()

        response = {'full_text': '', 'name': 'alsastatus'}
        response['full_text'] = "{title} {volume}".format(
            title=self.name, volume=volume)

        if mute:
            response['full_text'] = "{title} {mute} {volume}".format(
                title=self.name, mute=self.indicator, volume=volume)
            response['color'] = i3status_config['color_degraded']

        response['cached_until'] = time() + self.cache_timeout

        return response
