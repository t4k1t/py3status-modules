#!/usr/bin/env python

"""batterystatus

batterystatus is a battery monitoring module for py3status.
For upower support, batterystatus relies on slightly modified code from the
batti project.

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
from datetime import timedelta
from itertools import cycle
from os import path
import re
from time import time

import dbus
from dbus.exceptions import DBusException
from dbus.mainloop.glib import DBusGMainLoop


class BatteryInfo(object):

    def __init__(self, present=True, state="unknown", percentage=0, time=0):
        self._present = present
        self._state = state
        self._percentage = percentage
        self._time = time


class Data:
    """Aquire data."""

    dbus_service = 'org.freedesktop.UPower'
    dbus_object = '/org/freedesktop/UPower'
    device_iface = 'org.freedesktop.UPower.Device'
    property_iface = 'org.freedesktop.DBus.Properties'
    # Type 2 is `Battery`
    bat_type = 2

    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        try:
            self.__bus = dbus.SystemBus()
            iface = self._get_interface()
            self.devices = iface.EnumerateDevices()
            self.update_batteries()
            self.properties = dbus.Interface(iface, self.property_iface)
        except DBusException as e_upower:
            raise Exception("batterystatus: {0}".format(e_upower))

    def _get_interface(self):
        dkit_obj = self.__bus.get_object(self.dbus_service, self.dbus_object)
        return dbus.Interface(dkit_obj, self.dbus_service)

    def _get_battery(self, udi):
        battery_obj = self.__bus.get_object(self.dbus_service, udi)
        prop_iface = dbus.Interface(battery_obj, self.property_iface)
        dev_iface = dbus.Interface(battery_obj, self.device_iface)
        return (prop_iface, dev_iface)

    def update_batteries(self):
        batteries = []
        for dev in self.devices:
            (prop_iface, dev_iface) = self._get_battery(dev)
            dev_type = prop_iface.Get(self.device_iface, 'type')
            if dev_type == self.bat_type:
                batteries.append(dev)

        self.g = cycle(batteries)
        return batteries

    def get_state(self):
        battery = BatteryInfo()
        on_bat = self._on_battery()
        for dev in self.devices:
            (prop_iface, dev_iface) = self._get_battery(dev)
            dev_type = prop_iface.Get(self.device_iface, 'type')
            if dev_type == self.bat_type:
                _time = battery._time
                battery._present = prop_iface.Get(
                    self.device_iface, 'IsPresent')

                battery._state = prop_iface.Get(
                    self.device_iface, 'State')

                precise_charge = prop_iface.Get(
                    self.device_iface, 'Percentage')
                battery._percentage = int(float(str(precise_charge)))

                state = prop_iface.Get(self.device_iface, 'State')
                if state == 1:
                    battery._state = "charging"
                    _time = prop_iface.Get(
                        self.device_iface, 'TimeToFull')
                elif state == 2:
                    battery._state = "discharging"
                    _time = prop_iface.Get(
                        self.device_iface, 'TimeToEmpty')
                elif state == 3:
                    battery._state = "empty"
                elif state == 4:
                    battery._state = "full"
                else:
                    battery._state = "unknown"
                battery._time = timedelta(seconds=_time)

        return battery, on_bat

    def _on_battery(self):
        return self.properties.Get(self.device_iface, 'OnBattery')


class Py3status:

    def __init__(self):
        self.conf = self._read_config()
        self.data = Data()
        batteries = self.data.update_batteries()
        if len(batteries) > 1:
            setattr(Py3status, 'battery', self.batterystatus)

    def _read_config(self):
        """Read config file."""

        conf = {}
        config = SafeConfigParser({
            'title': 'BAT:', 'order': '0', 'interval': '0', 'threshold': '15',
            'format': '{bar} {percentage}%% {time}', 'alt_format': '{time}'})
        config.read([path.expanduser('~/.i3/py3status/modules.ini')])
        try:
            conf['title'] = config.get('batterystatus', 'title')
            conf['order'] = config.getint('batterystatus', 'order')
            conf['interval'] = config.getint('batterystatus', 'interval')
            conf['threshold'] = config.getint('batterystatus', 'threshold')
            conf['format'] = config.get('batterystatus', 'format')
            conf['alt_format'] = config.get('batterystatus', 'alt_format')
        except NoSectionError:
            conf['title'] = config.get('DEFAULT', 'title')
            conf['order'] = config.getint('DEFAULT', 'order')
            conf['interval'] = config.getint('DEFAULT', 'interval')
            conf['threshold'] = config.getint('DEFAULT', 'threshold')
            conf['format'] = config.get('DEFAULT', 'format')
            conf['alt_format'] = config.get('DEFAULT', 'alt_format')

        return conf

    def kill(self, json, i3status_config, event):
        """Handle termination."""

        pass

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""

        # Left mouse button
        if event['button'] == 1:
            pass
        # Middle mouse button
        # The default action for the middle button is refresh which actually
        # makes sense, so no need to override it.
        #elif event['button'] == 2:
        #    pass
        # Right mouse button
        elif event['button'] == 3:
            pass

    def _get_bar(self, percent, steps):
        bar = "["
        part = int(100 / steps)
        j = 0
        for i in range(0, percent, part):
            bar += "#"
        for j in range((len(bar) - 1), steps):
            bar += "."
        bar += "]"

        return bar

    def batterystatus(self, json, i3status_config):
        """Return response for i3status bar."""

        TITLE = self.conf['title']
        INTERVAL = self.conf['interval']
        ORDER = self.conf['order']
        THRESHOLD = self.conf['threshold']
        response = {'full_text': '', 'name': 'batterystatus'}

        pformat = self.conf['format']

        info, supplied = self.data.get_state()
        supply = ""
        if supplied == 0:
            supply = "~"
        TITLE += supply

        _time = ""
        if info._time.total_seconds() > 0:
            _time = str(info._time)

        # Apply formatting to output.
        r_dict = {
            '{percentage}': str(info._percentage),
            '{state}': info._state,
            '{onbattery}': supply,
            '{time}': str(_time),
            '{bar}': self._get_bar(info._percentage, 6),
        }
        robj = re.compile('|'.join(r_dict.keys()))
        data = (robj.sub(lambda m: r_dict[m.group(0)], pformat)).strip()
        state = info._state

        if state == 'charging':
            response['color'] = i3status_config['color_good']
        if state == 'discharging':
            response['color'] = i3status_config['color_degraded']
        if info._percentage <= THRESHOLD:
            response['color'] = i3status_config['color_bad']

        response['full_text'] = (
            "{title} {data}".format(
                title=TITLE, data=data))

        response['cached_until'] = time() + INTERVAL

        return (ORDER, response)
