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
# TODO
# * Add workaround for cards which cannot mute/unmute mixers


class AlsastatusException(Exception):
    """Custom taskstatus exception."""

    def __init__(self, exception):
        """Initialisation."""
        self.exception = exception

    def __str__(self):
        """Prepend message with 'alsastatus: '."""
        return "alsastatus: {exception}".format(exception=self.exception)


class Data:
    """Aquire data."""

    def __init__(self, mixer='Master'):
        """Initialise ALSA stuff."""
        self.volume = "-"
        self.mute = False
        self.mixer = mixer
        self.error = (None, None)

    def decrease_volume(self, step=3):
        """Decrease volume."""
        self.error = (None, None)

        try:
            check_output(
                ["amixer", "-q", "sset", self.mixer, "{}-".format(step)])
        except CalledProcessError as e:
            msg = "failed to decrease volume"
            self.error = (msg, time())
            raise AlsastatusException(msg + ": {}".format(str(e.output)))

    def increase_volume(self, step=3):
        """Increase volume."""
        self.error = (None, None)

        try:
            check_output(
                ["amixer", "-q", "sset", self.mixer, "{}+".format(step)],
                stderr=STDOUT)
        except CalledProcessError as e:
            msg = "failed to increase volume"
            self.error = (msg, time())
            raise AlsastatusException(msg + ": {}".format(str(e.output)))

    def toggle_mute(self):
        """Toggle mute."""
        self.error = (None, None)

        out = check_output(
            ["amixer", "get", self.mixer], stderr=STDOUT).splitlines()
        mute = out[-1].split()[5].strip(b'[]').decode('utf-8')  # whut?

        if mute == "on":
            try:
                check_output(
                    ["amixer", "-q", "sset", self.mixer, "mute"],
                    stderr=STDOUT)
            except CalledProcessError as e:
                msg = "failed to mute mixer"
                self.error = (msg, time())
                raise AlsastatusException(msg + ": {}".format(str(e.output)))
            else:
                self.mute = True
        else:
            try:
                check_output(
                    ["amixer", "-q", "sset", self.mixer, "unmute"],
                    stderr=STDOUT)
            except CalledProcessError:
                msg = "failed to unmute mixer"
                self.error = (msg, time())
                raise AlsastatusException(msg + ": {}".format(str(e.output)))
            else:
                self.mute = False

    def get_stats(self):
        """Return volume and mute status."""
        try:
            out = check_output(
                ["amixer", "get", self.mixer], stderr=STDOUT).splitlines()
        except CalledProcessError as e:
            msg = "failed to get mixer state"
            self.error = (msg, time())
            raise AlsastatusException(msg + ": {}".format(str(e.output)))
        except OSError as e:
            msg = "failed to execute amixer"
            self.error = (msg, time())
            raise AlsastatusException(msg + ": {}".format(str(e)))

        self.volume = out[-1].split()[3].strip(b'[]').decode('utf-8')  # whut?

        mute_str = out[-1].split()[5].strip(b'[]').decode('utf-8')  # whut?
        self.mute = mute_str == "off"

        return self.volume, self.mute


class Py3status:
    """This is where all the py3status magic happens."""

    cache_timeout = 0
    error_timeout = 10
    name = 'ALSA:'
    mixer = 'Master'
    step = 3
    indicator = '[M]'

    def __init__(self):
        """Initialise Data class."""
        self.data = None

    def _validate_config(self):
        """Validate configuration."""
        msg = []

        if type(self.error_timeout) != int or self.error_timeout < 0:
            msg.append("invalid error_timeout")
        if type(self.step) != int or self.step < 1 or self.step > 99:
            msg.append("invalid step")
        if type(self.name) != str:
            msg.append("invalid name")
        if type(self.mixer) != str or len(self.mixer) < 1:
            msg.append("invalid mixer")

        if msg:
            self.data.error = ("configuration error: {}".format(
                ", ".join(msg)), -1)

    def kill(self, json, i3status_config, event):
        """Handle termination."""
        pass

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        # Left click: Decrease volume
        if event['button'] == 1:
            self.data.decrease_volume(self.step)

        # Middle click: Mute/Unmute
        elif event['button'] == 2:
            self.data.toggle_mute()

        # Right click: Increase volume
        elif event['button'] == 3:
            self.data.increase_volume(self.step)

    def alsastatus(self, json, i3status_config):
        """Return response for i3status bar."""
        # Initialise Data class only once
        if not self.data:
            self.data = Data()
            self._validate_config()

        response = {'full_text': '', 'name': 'alsastatus'}

        # Reset error message
        # -1 means we can't recover from this error
        if (self.data.error[0] and
                (self.data.error[1] + self.error_timeout < time() and
                    self.data.error[1] != -1)):
            self.data.error = (None, None)

        if not self.data.error[0]:
            volume, mute = self.data.get_stats()

            response['full_text'] = "{title} {volume}".format(
                title=self.name, volume=volume)

            if mute:
                response['full_text'] = "{title} {mute} {volume}".format(
                    title=self.name, mute=self.indicator, volume=volume)
                response['color'] = i3status_config['color_degraded']
        else:
            response['full_text'] = "{title} {error}".format(
                title=self.name, error=self.data.error[0])
            response['color'] = i3status_config['color_bad']

        response['cached_until'] = time() + self.cache_timeout

        return response
