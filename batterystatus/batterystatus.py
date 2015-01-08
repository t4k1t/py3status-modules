#!/usr/bin/env python

"""batterystatus py3status module.

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

from datetime import timedelta
from itertools import cycle
import re
from time import time

import dbus
from dbus.exceptions import DBusException
from dbus.mainloop.glib import DBusGMainLoop


class BatteryInfo(object):

    """Base class containing battery info."""

    def __init__(self, present=True, state="unknown", percentage=0, time=0):
        """Initialise with some default values."""
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
        """Initialise dbus loop."""
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
        """Create dbus interface."""
        dkit_obj = self.__bus.get_object(self.dbus_service, self.dbus_object)
        return dbus.Interface(dkit_obj, self.dbus_service)

    def _get_battery(self, udi):
        """Get dbus interface for specific device."""
        battery_obj = self.__bus.get_object(self.dbus_service, udi)
        prop_iface = dbus.Interface(battery_obj, self.property_iface)
        dev_iface = dbus.Interface(battery_obj, self.device_iface)
        return (prop_iface, dev_iface)

    def update_batteries(self):
        """Load available batteries."""
        batteries = []
        for dev in self.devices:
            (prop_iface, dev_iface) = self._get_battery(dev)
            dev_type = prop_iface.Get(self.device_iface, 'type')
            if dev_type == self.bat_type:
                batteries.append(dev)

        self.g = cycle(batteries)
        return batteries

    def get_state(self):
        """Get battery info."""
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
        """Check if connected to power line."""
        return self.properties.Get(self.device_iface, 'OnBattery')


class Py3status:

    """This is where all the py3status magic happens."""

    cache_timeout = 0
    name = 'BATT:'
    threshold = 15
    format = '{bar} {percentage}%% {time}'
    alt_format = '{time}'

    def __init__(self):
        """Setup Data class, add additional batteries."""
        self.data = Data()
        batteries = self.data.update_batteries()
        battery_count = len(batteries)
        if battery_count == 0:
            setattr(Py3status, 'no_battery', True)
        elif battery_count > 1:
            setattr(Py3status, 'battery', self.batterystatus)

    def _get_bar(self, percent, steps):
        """Get power level representation in bar form."""
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
        response = {'full_text': '{title} no battery'.format(title=self.name),
                    'name': 'batterystatus'}
        NAME = self.name
        try:
            self.no_battery
            response['color'] = i3status_config['color_degraded']
            return response
        except AttributeError:
            pass

        pformat = self.format

        info, supplied = self.data.get_state()
        supply = ""
        if supplied == 0:
            supply = "~"
        NAME += supply

        _time = ""
        if info._time.total_seconds() > 0:
            _time = str(info._time)

        # Apply formatting to output.
        r_dict = {
            '%percentage': str(info._percentage),
            '%state': info._state,
            '%onbattery': supply,
            '%time': str(_time),
            '%bar': self._get_bar(info._percentage, 6),
        }
        robj = re.compile('|'.join(r_dict.keys()))
        data = (robj.sub(lambda m: r_dict[m.group(0)], pformat)).strip()
        state = info._state

        if state == 'charging':
            response['color'] = i3status_config['color_good']
        if state == 'discharging':
            response['color'] = i3status_config['color_degraded']
        if info._percentage <= self.threshold:
            response['color'] = i3status_config['color_bad']

        response['full_text'] = (
            "{title} {data}".format(
                title=NAME, data=data))

        response['cached_until'] = time() + self.cache_timeout

        return response
