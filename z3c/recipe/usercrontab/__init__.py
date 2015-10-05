# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

import logging
from z3c.recipe.usercrontab.usercrontab import UserCrontabManager


class UserCrontab:

    def __init__(self, buildout, name, options):
        self.options = options
        options['entry'] = '%s\t%s' % (options['times'], options['command'])
        self.comment = options.get('comment')
        # readcrontab and writecrontab are solely for testing.
        readcrontab = self.options.get('readcrontab', None)
        writecrontab = self.options.get('writecrontab', None)

        self.options['identifier'] = '%s [%s]' % (
            buildout['buildout']['directory'], name)
        self.crontab = UserCrontabManager(
            readcrontab, writecrontab,
            identifier=self.options['identifier'])

    def install(self):
        self.crontab.read_crontab()
        self.crontab.add_entry(self.options['entry'], self.comment)
        self.crontab.write_crontab()
        return ()

    def update(self):
        self.install()


def uninstall_usercrontab(name, options):
    readcrontab = options.get('readcrontab', None)
    writecrontab = options.get('writecrontab', None)

    identifier = options.get('identifier', 'NO IDENTIFIER')
    crontab = UserCrontabManager(
        readcrontab, writecrontab,
        identifier=identifier)
    crontab.read_crontab()
    nuked = crontab.del_entry(options['entry'])
    if nuked == 0:
        logging.getLogger(name).warning(
            "WARNING: Did not find a crontab-entry during uninstall; "
            "please check manually if everything was removed correctly")
    elif nuked > 1:
        logging.getLogger(name).error(
            "FATAL ERROR: Found more than one matching crontab-entry during "
            "uninstall; please resolve manually.\nMatched lines: %s",
            (options['entry']))
        raise RuntimeError(
            "Found more than one matching crontab-entry during uninstall")
    crontab.write_crontab()
