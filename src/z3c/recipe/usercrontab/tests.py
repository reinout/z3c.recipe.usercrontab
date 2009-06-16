# Copyright (c) 2007-2009 Zope Foundation and contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

import zc.buildout.testing

import unittest
import zope.testing
from zope.testing import doctest, renormalizing

from z3c.recipe.usercrontab import UserCrontabManager

usercrontab = UserCrontabManager(identifier='test')

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    usercrontab.read_crontab() # Store current user's real crontab.
    zc.buildout.testing.install_develop('z3c.recipe.usercrontab', test)

def tearDown(test):
    zc.buildout.testing.buildoutTearDown(test)
    usercrontab.write_crontab() # Restore current user's real crontab.

def test_suite():
    return unittest.TestSuite(doctest.DocFileSuite('README.txt', setUp=setUp,
                                                   tearDown=tearDown))
