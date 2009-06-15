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
import re


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


def dict_pmatch(d1, d2):
    """
    Returns true if all keys in d1 are in d2 and all values match
    """
    for k, v in d1.iteritems():
        if not (k in d2 and d2[k]==v):
            return False
    return True


env_re = re.compile(
    r'''
    ^            # Start of line
    (            # begin first group
    "[^"]*"      #   something enclosed in double quotes
    |\'[^\']*\'  #   OR something enclosed in single quotes
    |[^\s]+      #   OR some non-space-containing string
    )            # end first group

    \s*=\s*      # "=" surrounded by spaces

    (            # start second group
    "[^"]*"      #   something enclosed in double quotes
    |\'[^\']*\'  #   OR something enclosed in single quotes
    |[^"\']+     #   OR something that does not have quotes
    )?           # end of *optional* second group

    [^\s]*       # trailing whitespace
    $            # end of line
    ''',
    re.VERBOSE)



defaultreadcrontab = "crontab -l"
defaultwritecrontab = "crontab -"


class UserCrontabManager(object):
    """
    Helper class to edit entries in user crontabs (see man 5 crontab)
    """

    username = None
    crontab = []

    def __init__(self, readcrontab=None, writecrontab=None):
        self.readcrontab = readcrontab or defaultreadcrontab
        self.writecrontab = writecrontab or defaultwritecrontab

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

    def add_entry(self, entry, **env):
        """
        Add an entry to a crontab, if kw's are set, set environment args
        to be like that.
        """
        cur_env = {}
        new_crontab = []
        done = False

        for line in self.crontab:
            match = env_re.match(line)
            if match:
                # We have an environment statement ('MAILTO=something')
                env_key = match.group(1)
                env_value = match.group(2)
                cur_env[unescape_string(env_key)] = unescape_string(env_value)
            if (entry == line and
                'BUILDOUT' in env and
                'BUILDOUT' not in cur_env):
                # Possibly line we have to migrate post-0.4.
                temp_env = cur_env.copy()
                temp_env['BUILDOUT'] = env['BUILDOUT']
                if dict_pmatch(env, temp_env):
                    # Don't copy the entry, it will be added in the proper
                    # environment later.
                    pass
                else:
                    # Normal behaviour, just copy the line.
                    new_crontab.append(line)
            else:
                # Normal behaviour, just copy the line.
                new_crontab.append(line)
            if not done and dict_pmatch(env, cur_env):
                new_crontab.append(entry)
                done = True

        if (not done):
            for (k, v) in env.iteritems():
                if k not in cur_env or cur_env[k] != v:
                    if k == 'BUILDOUT':
                        # empty line for better between-buildout visual separation.
                        new_crontab.append('')
                    new_crontab.append('%s=%s' % (escape_string(k),
                                                  escape_string(v)))
            new_crontab.append(entry)

        self.crontab = new_crontab

    def del_entry(self, line):
        """
        Remove an entry from a crontab, dropping useless environment
        args at the end of the crontab, and which are replaced by
        something else before an actual crontab entry is found.

        (If the same entry occurs multiple times, it is removed several
         times)
        """
        new_crontab = []
        fresh_env = {}
        nuked = True
        dangling = True
        num_nuked = 0
        for l in reversed(self.crontab):
            m = env_re.match(l)
            if m:
                k, v = unescape_string(m.group(1)), unescape_string(m.group(2))
                if dangling:
                    continue
                if nuked is True:
                    if k in fresh_env:
                        continue
                fresh_env[k] = v
            else:
                if l==line:
                    nuked=True
                    num_nuked = num_nuked + 1
                    continue
                else:
                    if len(l.strip()):
                        dangling = False
                        nuked=False
                        fresh_env = {}
            new_crontab.append(l)
        self.crontab = [l for l in reversed(new_crontab)]
        return num_nuked
