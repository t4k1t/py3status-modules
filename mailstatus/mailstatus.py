#!/usr/bin/env python

"""mailstatus

Mailstatus is an email module for py3status.
It operates in two modes:
    'unread' mode: show number of unread mails
    'subject' mode: show subject of first unread email; on right click show
        subject of next unread mail

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
from email.header import decode_header
from mailbox import Maildir, NoSuchMailboxError
from os import path
from shlex import split
from time import time


class Data:
    """Aquire data."""

    def __init__(self, mailboxes):
        self.read_mailboxes(mailboxes)

    def decode_subject(self, subject):
        """Return decoded subject line."""
        decodedSub = ''
        for sub, enc in decode_header(subject):
            if enc is None:
                if isinstance(sub, str):
                    decodedSub += sub
                else:
                    decodedSub += sub.decode() + " "
            else:
                decodedSub += sub.decode(enc) + " "

        return decodedSub

    def read_mailboxes(self, mailboxes):
        """Return list of mailboxes.
        Exit on invalid mailbox.

        """
        mboxes = []
        if mailboxes:
            for mdir in mailboxes:
                try:
                    mboxes.append(Maildir(mdir, create=False))
                except NoSuchMailboxError:
                    raise Exception(
                        "mailstatus: %s doesn't appear to be a mailbox" % mdir)
                    exit(1)
        self.mboxes = mboxes

    def get_unread(self):
        """Return number of unread emails and a list containing the respective
        subjects.

        """
        unread = 0
        subjects = []
        if not self.mboxes:
            unread = 'no mailbox configured'

        for mbox in self.mboxes:
            for message in mbox:
                flags = message.get_flags()
                subject = message['subject']

                if not subject:
                    subject = "no subject"
                if 'S' not in flags:
                    unread += 1
                    decodedSub = self.decode_subject(subject)
                    subjects.append(decodedSub)

        return unread, subjects


class Py3status:

    def __init__(self):
        self.conf = self._read_config()
        self.data = Data(self.conf['mailboxes'])
        self.status = 'unread'
        self.currentSub = 0

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
        # Switch mode on middle click:
        if event['button'] == 2:
            if self.status == 'unread':
                self.status = 'subject'
            else:
                self.status = 'unread'
        # On right click increase index of subject list by one. This controls
        # which subject will be shown in 'subject' mode:
        if event['button'] == 3:
            if self.status == 'subject':
                self.currentSub += 1

    def mailstatus(self, json, i3status_config):
        """Return response for i3status bar."""
        title = self.conf['title']
        interval = self.conf['interval']
        order = self.conf['order']
        response = {'full_text': '', 'name': 'mailstatus'}
        unread, subjects = self.data.get_unread()

        if isinstance(unread, str):
            response['color'] = i3status_config['color_bad']
            response['full_text'] = "%s %s" % (
                title, unread)
        elif self.status == 'unread':
            if unread > 0:
                response['color'] = i3status_config['color_degraded']
            response['full_text'] = "%s %d" % (
                title, unread)
        else:
            # Carry over index of subject list:
            if self.currentSub >= len(subjects):
                self.currentSub = 0
            response['full_text'] = "%s %d: %s" % (
                title, self.currentSub, subjects[self.currentSub])

        response['cached_until'] = time() + interval

        return (order, response)
