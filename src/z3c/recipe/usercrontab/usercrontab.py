# Copyright (c) 2009 Zope Foundation and contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

import os


PREPEND = '# Generated by %s'
APPEND = '# END %s'


def escape_string(s):
    """
    Do a smart escape of string s, wrapping it in quotes and escaping
    those quotes if necessary. If the first or last byte is a space,
    also quote the string.
    """
    for c, d in (('"', "'"), ("'", '"')):
        if c in s:
            return '%s%s%s' % (d, s.replace(d, '\\'+d), d)
    if len(s)==0 or s[0].isspace() or s[-1].isspace():
        return '"%s"' % s

    return s


def unescape_string(s):
    """
    Unescape any escaped quotes, and remove quotes around the string
    """
    if len(s)==0:
        return s
    for c in ('"', "'"):
        if(s[0]==c and s[-1]==c):
            return s[1:-1].replace('\\'+c, c)
    return s


defaultreadcrontab = "crontab -l"
defaultwritecrontab = "crontab -"


class UserCrontabManager(object):
    """
    Helper class to edit entries in user crontabs (see man 5 crontab)
    """

    username = None
    crontab = []

    def __init__(self, readcrontab=None, writecrontab=None, identifier=None):
        self.readcrontab = readcrontab or defaultreadcrontab
        self.writecrontab = writecrontab or defaultwritecrontab
        assert identifier is not None
        self.append = APPEND % identifier
        self.prepend = PREPEND % identifier

    def read_crontab(self):
        self.crontab = [l.strip("\n") for l in
                        os.popen(self.readcrontab, "r")]

    def write_crontab(self):
        fd = os.popen(self.writecrontab, "w")
        for l in self.crontab:
            fd.write("%s\n" % l)
        fd.close()

    def __repr__(self):
        return "\n".join(self.crontab)

    def find_boundaries(self):
        # Migration: first zap all old BUILDOUT environment variables from
        # version 0.5.  A bit rude to do it here, but the feature was only
        # released for a couple of hours.
        self.crontab = [line for line in self.crontab
                        if not line.startswith('BUILDOUT=')]

        start = None
        end = None
        old_warning_marker = None
        for line_number, line in enumerate(self.crontab):
            if line.strip() == self.prepend:
                if start is not None:
                    raise RuntimeError("%s found twice in the same crontab. "
                                       "Fix by hand." % self.prepend)
                start = line_number
            if line.strip() == self.append:
                if end is not None:
                    raise RuntimeError("%s found twice in the same crontab. "
                                       "Fix by hand." % self.append)
                end = line_number + 1
                # ^^^ +1 as we want the range boundary and that is behind the
                # element.
            if line.startswith('WARNING='):
                old_warning_marker = line_number
        return start, end, old_warning_marker

    def add_entry(self, entry):
        """Add an entry to the crontab.

        Find lines enclosed by APPEND/PREPEND, zap and re-add.

        """
        start, end, old_warning_marker = self.find_boundaries()
        inject_at = -1 # By default at the end of the file.
        if old_warning_marker:
            # At least in front of the old warning marker.
            inject_at = old_warning_marker
        if start is not None and end is not None:
            # But preferably in our existing location.
            self.crontab[start:end] = []
            inject_at = start

        to_inject = ['', self.prepend, entry, self.append, '']
        if inject_at == -1:
            # [-1:-1] would inject before the last item...
            self.crontab += to_inject
        else:
            self.crontab[inject_at:inject_at] = to_inject

    def del_entry(self, entry):
        """Remove an entry from a crontab.

        Drop now-useless WARNING environment if it is the last one in the
        file.

        """
        start, end, old_warning_marker = self.find_boundaries()
        if start is not None and end is not None:
            if start > 0:
                if not self.crontab[start - 1].strip():
                    # Also strip empty line in front.
                    start = start - 1
            if end < len(self.crontab):
                if not self.crontab[end].strip():
                    # Also strip empty line after end marker.
                    # Note: not self.crontab[end + 1] as end is the location
                    # AFTER the end marker to selected it with [start:end].
                    end = end + 1
            if end == len(self.crontab):
                end = None # Otherwise the last line stays in place
            self.crontab[start:end] = []
            return 1 # Number of entries that are removed.

        if old_warning_marker is not None:
            old = len(self.crontab[old_warning_marker:])
            self.crontab[old_warning_marker:] = [
                line for line in self.crontab[old_warning_marker:]
                 if line != entry]
            new = len(self.crontab[old_warning_marker:])

            # Cleanup when possible
            remaining = [line for line in self.crontab[old_warning_marker:]
                         if line.strip()]
            if len(remaining) == 1:
                # Just the WARNING marker, so remove everything.
                self.crontab[old_warning_marker:] = []

            return old - new

        # Nothing removed.
        return 0
