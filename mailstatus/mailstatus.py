#!/usr/bin/env python

"""mailstatus is an email module for py3status.
It operates in two modes:
    'unread' mode: show number of unread mails
    'subject' mode: show subject of first unread email; on right click show
        subject of next unread mail
"""

from time import time
from mailbox import Maildir, NoSuchMailboxError
from email.header import decode_header

class _Data:
    """Aquire data."""

    def decode_subject(self, subject):
        """Return decoded subject line."""
        decodedSub = ''
        for sub, enc in decode_header(subject):
            if enc == None:
                if isinstance(sub, str):
                    decodedSub += sub
                else:
                    decodedSub += sub.decode() + " "
            else:
                decodedSub += sub.decode(enc) + " "

        return decodedSub

    def read_maildirs(self):
        """
        CONFIGURATION
        """
        MAILDIRS = [
            'path/to/mailbox',
            ]

        """Return list of mailboxes.
        Exit on invalid mailbox.
        """
        mboxes = []
        for mdir in MAILDIRS:
            try:
                mboxes.append(Maildir(mdir, create=False))
            except NoSuchMailboxError:
                print("\n%s doesn't appear to be a mailbox.\n" % mdir)
                exit(1)

        return mboxes

    def get_unread(self):
        """Return number of unread emails and a list containing the respective
        subjects.
        """
        unread = 0
        subjects = []
        mboxes = self.read_maildirs()

        for mbox in mboxes:
            for message in mbox:
                flags = message.get_flags()
                subject = message['subject']

                status = ""

                if not subject:
                    subject = "no subject"
                if 'S' not in flags:
                    decodedSub = self.decode_subject(subject)
                    unread += 1
                    subjects.append(decodedSub)

        return unread, subjects


class Py3status:

    def __init__(self):
        self.status = 'unread'
        self.currentSub = 0

    def on_click(self, json, i3status_config, event):
        """Handle mouse clicks."""
        # Switch mode on middle click:
        if event['button'] == 2:
            if self.status == 'unread':
                self.status = 'subject'
            else:
                self.status = 'unread'
        # On right click increase index of subject list by one. This controls
        # wich subject will be shown in 'subject' mode:
        if event['button'] == 3:
            self.currentSub += 1

    def mailinfo(self, json, i3status_config):
        """Return response for i3status bar."""
        data = _Data()
        response = {'full_text': '', 'name': 'mailinfo'}
        unread, subjects = data.get_unread()

        if self.status == 'unread':
            if unread > 0:
                response['color'] = i3status_config['color_degraded']
            response['full_text'] = "✉ %d" % \
                    (unread)
        else:
            # Carry over index of subject list:
            if self.currentSub >= len(subjects):
                self.currentSub = 0
            response['full_text'] = "✉ %d: %s" % \
                    (self.currentSub, subjects[self.currentSub])

        response['cached_until'] = time()

        return (0, response)
