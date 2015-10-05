z3c.recipe.usercrontab changes
==============================

1.4 (unreleased)
----------------

- Nothing changed yet.


1.3 (2015-10-05)
----------------

- New 'comment' option. This way you can add a small explanatory one-line
  option to your crontab entry.
  [reinout]


1.2.1 (2015-09-11)
------------------

- Moved development to https://github.com/reinout/z3c.recipe.usercrontab
  [reinout]

- Made a few small fixes to get everything running on python 3.
  [reinout]


1.1 (2010-11-09)
----------------

- Append and prepend less white space per cron item, so you do not get
  increasing extra white space everytime you run bin/buildout.
  [maurits]


1.0 (2009-11-10)
----------------

- Only small documentation changes; version bumped to 1.0 to signal
  stability.  [reinout]


0.7 (2009-08-24)
----------------

- The crontab now gets checked every time buildout runs, not only when there's
  a change in the configuration.  [reinout]


0.6.1 (2009-06-17)
------------------

- Documentation fixes.  [reinout]


0.6 (2009-06-16)
----------------

- Removed essentially-unused complete environment variable handling.
  [reinout]

- Adding our entries with descriptive comments now: it includes the buildout
  file and the part name.  [reinout]


0.5.1 (2009-06-16)
------------------

- Reverted the "BUILDOUT=..." environment variable, including migration.  I'll
  add a better way after this release.  [reinout]


0.5 (2009-06-15)
----------------

* Added migration code for pre-0.5 entries without a BUILDOUT variable.
  [reinout]

* Added extra blank line in front of "BUILDOUT=..." variable to allow for
  better readability.  [reinout]

* Added "BUILDOUT=...." as environment variable for every set of crontab lines
  handled by one buildout.  This makes it much easier to spot what got added
  by which buildout (in case you have multiple) or which buildout at all (if
  you have no clue where the buildout can be found).  [reinout]

0.4 (2008-02-25)
----------------

* Fix bug where UserCrontabs with empty readcrontab and writecrontab
  constructor arguments where broken

0.3 (2008-02-23)
----------------

* Renamed to z3c.recipe.usercrontab
* Add an option to change the command used to read and write crontabs
* Improved tests to not modify the real crontab

0.2 (2008-01-12)
----------------

* Warn if an entry cannot be removed in buildout uninstall
* Break if multiple entries would be removed in buildout uninstall
* Have del_entry return the number of removed

0.1 (2008-01-12)
----------------

* Initial release.
