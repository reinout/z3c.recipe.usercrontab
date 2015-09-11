# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

import os
from setuptools import setup, find_packages

version = '1.2dev'
name = 'z3c.recipe.usercrontab'

def read(*rnames):
    return open(os.path.join(*rnames)).read()

setup(name=name,
      version=version,
      author='The Health Agency',
      author_email='techniek@thehealthagency.com',
      license='ZPL',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Framework :: Buildout",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Build Tools",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: Zope Public License"
          ],
      description="User Crontab install buildout recipe",
      long_description=(read('README.rst') +
                        '\n\n' +
                        read('src/z3c/recipe/usercrontab/README.rst') +
                        '\n\n' +
                        read('CHANGES.rst')),
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['z3c', 'z3c.recipe'],
      include_package_data=True,
      install_requires=['setuptools', 'zc.buildout'],
      extras_require = dict(test=['zope.testing']),
      entry_points={
          'zc.buildout': ['default = %s:UserCrontab' % name],
          'zc.buildout.uninstall': ['default = %s:uninstall_usercrontab' % name]
      }
      )
