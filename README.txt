======================
z3c.recipe.usercrontab
======================

The problem
===========

When deploying applications, it can be useful to have maintenance
tasks be started periodically. On Unix platforms this is usually done
using ``cron`` which starts `cronjobs`. Adding cronjobs to the
system-wide cron directory (for example by placing a file in
``/etc/cron.d``) can be handled using the ``zc.recipe.deployment``
package, but it does not support adding cronjobs by normal
users. (as ``/etc/cron.d`` usually is world-writable).

The solution
============
``z3c.recipe.usercrontab`` interfaces with cron using ``crontab(1)``,
and allows normal users to install their own cronjobs. This is done by
having buildout add and remove cronjobs when installing and
uninstalling packages.

How to use it
=============

To use ``z3c.recipe.usercrontab`` you need to add the following to
your buildout.cfg::

 [mycronjob]
 recipe = z3c.recipe.usercrontab
 times = 0 12 * * *
 command = echo nothing happens at noon

and finally add ``mycronjob`` to the ``parts`` line(s) of your
buildout.cfg


Credits
=======

Original authors: Jasper Spaans and Jan-Jaap Driessen at `The Health Agency
<http://www.thehealthagency.com>`_.

Most recent versions: `Reinout van Rees <http://reinout.vanrees.org>`_, also
at `The Health Agency <http://www.thehealthagency.com>`_
