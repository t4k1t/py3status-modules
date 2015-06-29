#!/usr/bin/env python

"""taskstatus py3status module.

taskstatus is a taskwarrior module for py3status.
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

from subprocess import check_output, CalledProcessError, STDOUT
from time import time


class TaskstatusException(Exception):

    """Custom taskstatus exception."""

    def __init__(self, exception):
        """Initialisation."""
        self.exception = exception

    def __str__(self):
        """Prepend message with 'taskstatus: '."""
        return "taskstatus: {exception}".format(exception=self.exception)


class Data:

    """Aquire data."""

    def __init__(self):
        """Initialise."""
        self.error = (None, None)

    def get_tasks(self):
        """Return number of open and overdue tasks as tuple."""
        tasks = 0
        overdue = 0

        stats = check_output(["task", "stats"]).split()
        tasks = int(stats[5])

        try:
            overdueList = check_output(
                ["task", "overdue"], stderr=STDOUT).split()
            overdue = int(overdueList[len(overdueList)-2])
        except CalledProcessError as e:
            if b"No matches" not in e.output:
                raise TaskstatusException("failed to execute 'task overdue'")
        except OSError:
            raise TaskstatusException("failed to execute 'task overdue'")

        return tasks, overdue


class Py3status:

    """Called by py3status."""

    cache_timeout = 0
    error_timeout = 10
    name = 'TASK:'
    data = None

    def __init__(self):
        """Read config, initialise Data class."""
        # See if we can find taskwarrior.
        try:
            check_output(["task", "--version"], stderr=STDOUT)
        except OSError:
            raise TaskstatusException("failed to execute 'task'")
        self.data = Data()

    def _validate_config(self):
        """Validate configuration."""
        msg = []

        if type(self.name) != str:
            msg.append("invalid name")

        if msg:
            self.data.error = ("configuration error: {}".format(
                ", ".join(msg)), -1)

    def taskstatus(self, json, i3status_config):
        """Return response for py3status."""
        response = {'full_text': '', 'name': 'taskstatus'}

        # Reset error message
        # -1 means we can't recover from this error
        if (self.data.error[0] and
                (self.data.error[1] + self.error_timeout < time() and
                    self.data.error[1] != -1)):
            self.data.error = (None, None)

        tasks, overdue = self.data.get_tasks()

        if overdue > 0:
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s %d/%d" % \
                (self.name, overdue, tasks)
        else:
            response['full_text'] = "%s %d" % \
                (self.name, tasks)

        response['cached_until'] = time() + self.cache_timeout

        return response
