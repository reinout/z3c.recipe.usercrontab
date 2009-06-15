# Copyright (c) 2009 Zope Foundation and contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

The recipe z3c.recipe.usercrontab is a small recipe to facilitate the
installing of cronjobs into user crontabs.

    >>> from z3c.recipe.usercrontab.usercrontab import UserCrontabManager
    >>> c = UserCrontabManager()


Entry and environment handling
------------------------------

For these tests, we fake a crontab by filling the list of cron entries
for this object:

    >>> c.crontab = [ 'MAILTO=""', '@reboot echo "No-one will see this"']
    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"

Now, we're adding a method to it using the official way:

    >>> c.add_entry('@reboot echo "example.com gets spammed!"',
    ...             MAILTO="example@example.com")

The object also has a convenient __repr__, so we can test its output:

    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"
    MAILTO=example@example.com
    @reboot echo "example.com gets spammed!"

Adding another entry with yet another MAILTO line is placed at the end:

    >>> c.add_entry('@reboot echo "example.com gets spammed twice!"',
    ...              MAILTO="twice@example.com")
    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"
    MAILTO=example@example.com
    @reboot echo "example.com gets spammed!"
    MAILTO=twice@example.com
    @reboot echo "example.com gets spammed twice!"

When another entry is made with the same MAILTO, the MAILTO clause is
not repeated again:

    >>> c.add_entry('@reboot echo "twice@example.com gets spammed twice!"',
    ...             MAILTO="twice@example.com")
    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"
    MAILTO=example@example.com
    @reboot echo "example.com gets spammed!"
    MAILTO=twice@example.com
    @reboot echo "twice@example.com gets spammed twice!"
    @reboot echo "example.com gets spammed twice!"

Removing entries also works, and removes superfluous environment variables:

    >>> c.del_entry('@reboot echo "example.com gets spammed!"') == 1
    True
    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"
    MAILTO=twice@example.com
    @reboot echo "twice@example.com gets spammed twice!"
    @reboot echo "example.com gets spammed twice!"

Removing entries does not remove too much:

    >>> c.del_entry('@reboot echo "twice@example.com gets spammed twice!"') == 1
    True
    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"
    MAILTO=twice@example.com
    @reboot echo "example.com gets spammed twice!"

Removing the last entry also removes the dangling MAILTO line:

    >>> c.del_entry('@reboot echo "example.com gets spammed twice!"') == 1
    True
    >>> print c
    MAILTO=""
    @reboot echo "No-one will see this"

Removing the final entry removes the remaining MAILTO line, leaving us
with an empty list:

    >>> c.del_entry('@reboot echo "No-one will see this"') == 1
    True
    >>> len(c.crontab)
    0

Adding an entry without a MAILTO environment line also doesn't put in
an empty one:

    >>> c.add_entry('@reboot echo "Someone will see this"')
    >>> print c
    @reboot echo "Someone will see this"

Adding an entry with an empty MAILTO line adds it at the end, so the
first entry is not disturbed:

    >>> c.add_entry('@reboot echo "No-one will see this"', MAILTO="")
    >>> print c
    @reboot echo "Someone will see this"
    MAILTO=""
    @reboot echo "No-one will see this"

When introducing a new environment variable to leave markers which buildout is
used, the mix between the environment is right:

    >>> c.crontab = ['MAILTO=""', 'BUILDOUT=my/path', '@reboot echo "no mailto, my/path"']
    >>> print c
    MAILTO=""
    BUILDOUT=my/path
    @reboot echo "no mailto, my/path"
    >>> c.add_entry('@reboot echo "no mailto, my/other"', MAILTO="", BUILDOUT="my/other")
    >>> print c
    MAILTO=""
    BUILDOUT=my/path
    @reboot echo "no mailto, my/path"
    BUILDOUT=my/other
    @reboot echo "no mailto, my/other"
    >>> c.add_entry('@reboot echo "no mailto, my/other, bla"', MAILTO="", BUILDOUT="my/other")
    >>> print c
    MAILTO=""
    BUILDOUT=my/path
    @reboot echo "no mailto, my/path"
    BUILDOUT=my/other
    @reboot echo "no mailto, my/other, bla"
    @reboot echo "no mailto, my/other"
    >>> c.add_entry('@reboot echo "mailto example, my/path"',
    ...             MAILTO="something@example.com", BUILDOUT="my/path")
    >>> print c
    MAILTO=""
    BUILDOUT=my/path
    @reboot echo "no mailto, my/path"
    BUILDOUT=my/other
    @reboot echo "no mailto, my/other, bla"
    @reboot echo "no mailto, my/other"
    MAILTO=something@example.com
    BUILDOUT=my/path
    @reboot echo "mailto example, my/path"

Adding an extra environment variable to an existing entry results in a second
entry, but with the extra environment variable.  This is technically correct,
but it might warrant an exception. TODO.

    >>> c.add_entry('@reboot echo "mailto example, my/path"',
    ...             MAILTO="something@example.com", BUILDOUT="my/path",
    ...             BLA='bla')
    >>> print c
    MAILTO=""
    BUILDOUT=my/path
    @reboot echo "no mailto, my/path"
    BUILDOUT=my/other
    @reboot echo "no mailto, my/other, bla"
    @reboot echo "no mailto, my/other"
    MAILTO=something@example.com
    BUILDOUT=my/path
    @reboot echo "mailto example, my/path"
    BLA=bla
    @reboot echo "mailto example, my/path"


Read/write crontab methods
--------------------------

Next, test the read_crontab and write_crontab methods; we'll use
``cat`` and a temporary file to not modifiy the crontab of the user
running these tests:

    >>> import tempfile
    >>> t = tempfile.NamedTemporaryFile('w')
    >>> crontestfile = t.name
    >>> t.write("#dummy\n")

    >>> c = UserCrontabManager(readcrontab="cat %s" % crontestfile,
    ...                        writecrontab="cat >%s" % crontestfile)
    >>> c.read_crontab()
    >>> a = repr(c)
    >>> c.add_entry('# improbable entry')
    >>> c.write_crontab()
    >>> c.read_crontab()
    >>> b =repr(c)
    >>> a == b
    False

Now, delete this entry again and make sure the old crontab is restored:

    >>> c.del_entry('# improbable entry') == 1
    True
    >>> c.write_crontab()
    >>> c.read_crontab()
    >>> b = repr(c)
    >>> a == b
    True


Buildout recipe usage
---------------------

Do the buildout shuffle:

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = foo
    ...
    ... [foo]
    ... recipe = z3c.recipe.usercrontab
    ... times = # @reboot
    ... command = echo nothing happens
    ... readcrontab = cat %(crontest)s
    ... writecrontab = cat >%(crontest)s
    ...
    ... [bar]
    ... recipe = z3c.recipe.usercrontab
    ... times = # @reboot
    ... command = echo nothing happens
    ... readcrontab = cat %(crontest)s
    ... writecrontab = cat >%(crontest)s
    ... ''' % ( { 'crontest': crontestfile } ))


    >>> import os
    >>> print system(os.path.join('bin', 'buildout'))
    Installing foo.
    <BLANKLINE>

Check that it really was added to the crontab:

    >>> c.read_crontab()
    >>> b = repr(c)
    >>> a == b
    False

    >>> '# @reboot\techo nothing happens' in c.crontab
    True

    >>> 'WARNING=The entries below were generated by buildout, do not modify' in c.crontab
    True

The entries are grouped per buildout (with a blank line in front of every
BUILDOUT line for better readability):

    >>> print c # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    WARNING=The entries below were generated by buildout, do not modify
    <BLANKLINE>
    BUILDOUT=.../sample-buildout
    # @reboot   echo nothing happens

Uninstall the recipe:

    >>> print system(os.path.join('bin', 'buildout')+' buildout:parts=')
    Uninstalling foo.
    Running uninstall recipe.
    <BLANKLINE>

And check that its entry was removed (i.e., the contents of the
crontab are the same as when this test was started; in any case, the
teardown from the testrunner makes sure the old situation is
restored):

    >>> c.read_crontab()
    >>> b = repr(c)
    >>> a == b
    True

Now, break it by adding the same crontab entry twice:

    >>> print system(os.path.join('bin', 'buildout')+' "buildout:parts=foo bar"')
    Installing foo.
    Installing bar.
    <BLANKLINE>

    >>> print system(os.path.join('bin', 'buildout')+' buildout:parts=') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Uninstalling bar.
    Running uninstall recipe.
    bar: FATAL ERROR: Found more than one matching crontab-entry during uninstall; please resolve manually.
    Matched lines: # @reboot echo nothing happens
    While:
      Installing.
      Uninstalling bar.
    <BLANKLINE>
    An internal error occured due to a bug in either zc.buildout or in a
    recipe being used:
    Traceback (most recent call last):
    ...
    RuntimeError: Found more than one matching crontab-entry during uninstall
    <BLANKLINE>

Manually fix it by removing the offending lines:

    >>> c.read_crontab()
    >>> c.del_entry("# @reboot\techo nothing happens")
    2
    >>> c.write_crontab()

And now we can uninstall again (albeit with some warnings):

    >>> print system(os.path.join('bin', 'buildout')+' buildout:parts=') # doctest:
    Uninstalling bar.
    Running uninstall recipe.
    bar: WARNING: Did not find a crontab-entry during uninstall; please check manually if everything was removed correctly
    Uninstalling foo.
    Running uninstall recipe.
    foo: WARNING: Did not find a crontab-entry during uninstall; please check manually if everything was removed correctly
    <BLANKLINE>
