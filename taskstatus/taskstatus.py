#!/usr/bin/env python

"""taskstatus

Taskstatus is a taskwarrior module for py3status.
It shows the number of open tasks in your py3status bar.

Copyright (C) 2013  Tablet Mode

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

from time import time
from subprocess import check_output, CalledProcessError, STDOUT
from sys import stderr

class _Data:
    """Aquire data."""

    def get_tasks(self):
        """Return number of overdue tasks and number of open tasks."""
        tasks = 0
        overdue = 0

        stats = check_output(["task", "stats"]).split()
        tasks = int(stats[5])

        try:
            overdueList = check_output(["task", "overdue"], stderr=STDOUT).split()
            overdue = int(overdueList[len(overdueList)-2])
        except CalledProcessError:
            overdue = -1
        except OSError:
            stderr.write("\ntaskwarrior: failed to execute 'task overdue'\n")
            exit(1)

        return tasks, overdue


class Py3status:
    """Called by py3status."""

    def __init__(self):
        # check if taskwarrior is installed
        try:
            check_output(["task", ""], stderr=STDOUT)
        except OSError:
            stderr.write("\ntaskwarrior: failed to execute 'task'\n")
            exit(1)
        self.data = _Data()

    def taskstatus(self, json, i3status_config):
        """Return response for py3status."""
        response = {'full_text': '', 'name': 'taskinfo'}

        tasks, overdue = self.data.get_tasks()

        if tasks > 0:
            response['full_text'] = "✓ %d" % \
                (tasks)
        if overdue > 0:
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "✓ %d/%d" % \
                (overdue, tasks)

        response['cached_until'] = time() + 120

        return (0, response)
