#!/usr/bin/env python

"""taskstatus

Taskstatus is a taskwarrior module for py3status.
It shows the number of open tasks in your py3status bar.

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
from os import path
from shlex import split
from subprocess import check_output, CalledProcessError, STDOUT
from sys import stderr
from time import time

class _Data:
    """Aquire data."""

    def read_config(self):
        """Read config file.
        Exit on invalid config.
        """
        config = SafeConfigParser({'title': 'TASK:', 'order': '0',
            'interval': '0'})
        config.read([path.expanduser('~/.i3/py3status/modules.ini')])
        try:
            self.TITLE = split(config.get('taskstatus', 'title'))[0]
            self.ORDER = config.getint('taskstatus', 'order')
            self.INTERVAL = config.getint('taskstatus', 'interval')
        except NoSectionError:
            stderr.write("\ntaskstatus: no taskstatus section in config\n\n")
            self.TITLE = split(config.get('DEFAULT', 'title'))[0]
            self.ORDER = config.getint('DEFAULT', 'order')
            self.INTERVAL = config.getint('DEFAULT', 'interval')

    def get_tasks(self):
        """Return number of overdue tasks and number of open tasks."""
        tasks = 0
        overdue = 0

        stats = check_output(["task", "stats"]).split()
        tasks = int(stats[5])

        try:
            overdueList = check_output(["task", "overdue"], \
                    stderr=STDOUT).split()
            overdue = int(overdueList[len(overdueList)-2])
        except CalledProcessError:
            overdue = -1
        except OSError:
            stderr.write("\ntaskwarrior: failed to execute 'task overdue'\n\n")
            exit(1)

        return tasks, overdue


class Py3status:
    """Called by py3status."""

    def __init__(self):
        # check if taskwarrior is installed
        try:
            check_output(["task", "--version"], stderr=STDOUT)
        except OSError:
            stderr.write("\ntaskwarrior: failed to execute 'task'")
            exit(1)
        self.data = _Data()
        self.data.read_config()

    def taskstatus(self, json, i3status_config):
        """Return response for py3status."""
        response = {'full_text': '', 'name': 'taskstatus'}

        tasks, overdue = self.data.get_tasks()

        if overdue > 0:
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s %d/%d" % \
                (self.data.TITLE, overdue, tasks)
        else:
            response['full_text'] = "%s %d" % \
                (self.data.TITLE, tasks)

        response['cached_until'] = time() + self.data.INTERVAL

        return (self.data.ORDER, response)
