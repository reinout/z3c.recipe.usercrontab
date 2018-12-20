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

version = '1.5'
name = 'z3c.recipe.usercrontab'


def read(*rnames):
    with open(os.path.join(*rnames)) as f:
        return f.read()


setup(name=name,
      version=version,
      author='Reinout van Rees',
      author_email='reinout@vanrees.org',
      url='https://github.com/reinout/z3c.recipe.usercrontab',
      license='ZPL',
      classifiers=[
          "Development Status :: 6 - Mature",
          "Framework :: Buildout",
          "Intended Audience :: Developers",
          "Topic :: Software Development",
          "Topic :: Software Development :: Build Tools",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved",
          "License :: OSI Approved :: Zope Public License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ],
      description="User Crontab install buildout recipe",
      long_description='\n\n'.join([
          read('README.rst'),
          read('z3c/recipe/usercrontab/README.rst'),
          read('CHANGES.rst')]),
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['z3c', 'z3c.recipe'],
      include_package_data=True,
      install_requires=['setuptools', 'zc.buildout'],
      extras_require={'test': ['zope.testing']},
      entry_points={
          'zc.buildout': ['default = %s:UserCrontab' % name],
          'zc.buildout.uninstall': [
              'default = %s:uninstall_usercrontab' % name]
      }
      )
