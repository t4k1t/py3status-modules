#!/usr/bin/env python

"""mailstatus

Mailstatus is an email module for py3status.
It shows the number of unread mails in your mailboxes.

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

from configparser import SafeConfigParser, NoOptionError, NoSectionError
from mailbox import Maildir, NoSuchMailboxError
from os import listdir, path
from shlex import split
from time import time


class Data:
    """Aquire data."""

    def __init__(self, mailboxes):
        self.read_mailboxes(mailboxes)

    def read_mailboxes(self, mailboxes):
        """Return list of mailboxes.
        Exit on invalid mailbox.

        """
        mboxes = []
        state = []
        unread = []
        if mailboxes:
            for mdir in mailboxes:
                try:
                    mboxes.append(Maildir(mdir, create=False))
                    state.append('')
                    unread.append(0)
                except NoSuchMailboxError:
                    raise Exception(
                        "mailstatus: %s doesn't appear to be a mailbox" % mdir)
                    exit(1)
        self.mboxes = mboxes
        self.mbox_state = state
        self.unread = unread

    def get_unread_maildir(self, mbox):
        mdir = mbox._paths['new']
        unread = len(
            [item for item in listdir(mdir) if path.isfile(path.join(
                mdir, item))])
        return unread

    def get_unread(self):
        """Return number of unread emails."""
        unread_mails = 0
        if not self.mboxes:
            unread_mails = 'no mailbox configured'
            return unread_mails

        last_state = self.mbox_state[:]
        unread_per_box = self.unread[:]
        ct = 0
        for mbox in self.mboxes:
            mbox.keys()
            self.mbox_state[ct] = mbox._toc
            if self.mbox_state[ct] == last_state[ct]:
                pass
            else:
                unread_per_box[ct] = 0
                if isinstance(mbox, Maildir):
                    unread_per_box[ct] = self.get_unread_maildir(mbox)
                else:
                    for message in mbox:
                        flags = message.get_flags()
                        if 'S' not in flags:
                            unread_per_box[ct] += 1
            ct += 1
        for mail in unread_per_box:
            unread_mails += mail
        self.unread = unread_per_box

        return unread_mails


class Py3status:

    def __init__(self):
        self.conf = self._read_config()
        self.data = Data(self.conf['mailboxes'])
        self.status = 'unread'

    def _read_config(self):
        """Read config file."""
        conf = {}
        config = SafeConfigParser({
            'title': 'MAIL:', 'order': '0', 'interval': '0'})
        config.read([path.expanduser('~/.i3/py3status/modules.ini')])

        try:
            conf['mailboxes'] = split(config.get('mailstatus', 'mailboxes'))
            conf['title'] = split(config.get('mailstatus', 'title'))[0]
            conf['order'] = config.getint('mailstatus', 'order')
            conf['interval'] = config.getint('mailstatus', 'interval')
        except NoSectionError:
            raise Exception("mailstatus: no mailstatus section in config")
            conf['mailboxes'] = False
            conf['title'] = split(config.get('DEFAULT', 'title'))[0]
            conf['order'] = config.getint('DEFAULT', 'order')
            conf['interval'] = config.getint('DEFAULT', 'interval')
        except NoOptionError:
            raise Exception("mailstatus: no mailboxes configured")

        return conf

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        pass

    def mailstatus(self, json, i3status_config):
        """Return response for i3status bar."""
        title = self.conf['title']
        interval = self.conf['interval']
        order = self.conf['order']
        response = {'full_text': '', 'name': 'mailstatus'}
        unread = self.data.get_unread()

        if isinstance(unread, str):
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s %s" % (
                title, unread)
        else:
            if unread > 0:
                response['color'] = i3status_config['color_degraded']
            response['full_text'] = "%s %d" % (
                title, unread)

        response['cached_until'] = time() + interval

        return (order, response)
