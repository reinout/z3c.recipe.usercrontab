# Copyright (c) 2007-2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

from zope.testing import renormalizing

import doctest
import unittest
import zc.buildout.testing


optionflags = (doctest.ELLIPSIS
               | doctest.NORMALIZE_WHITESPACE
               | doctest.REPORT_NDIFF)


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('z3c.recipe.usercrontab', test)
    # Install any other recipes that should be available in the tests

    # Store current user's real crontab.
    from z3c.recipe.usercrontab import UserCrontabManager
    test.usercrontab = UserCrontabManager(identifier='test')
    test.usercrontab.read_crontab()


def tearDown(test):
    zc.buildout.testing.buildoutTearDown(test)
    # Restore current user's real crontab.
    test.usercrontab.write_crontab()


def test_suite():
    suite = unittest.TestSuite((
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp,
            tearDown=tearDown,
            optionflags=optionflags,
            checker=renormalizing.RENormalizing([
                # If want to clean up the doctest output you
                # can register additional regexp normalizers
                # here. The format is a two-tuple with the RE
                # as the first item and the replacement as the
                # second item, e.g.
                # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                zc.buildout.testing.normalize_path,
                ]),
            ),
        ))
    return suite
