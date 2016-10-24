===============
Freewvs Wrapper
===============

This is a wrapper around freewvs, a free web vulnerability scanner.
The wrapper parses the resulting xml into csv and sends it via email to
subscribers.

Freewvs searchs scripts and applications within a directory and try to
recognize them. If a script or application is recognized freewvs will try to
extract the version and after that it searchs in a database if there are
known security holes or vulnerabilities.
At the end a xml report will be generated with all vulnerable
scripts/applications in it.


INSTALLATION
============

- First, install python-lxml, git and subversion.
- Clone this repository to any directory and clone freewvs into the
  subdirectory ``freewvs``.

.. code-block:: Bash

  mkdir -p /opt/freewvs
  cd /opt/freewvs
  git clone https://github.com/adfinis-sygroup/freewvs-wrapper .
  svn checkout https://svn.schokokeks.org/repos/freewvs
  cp settings.example.py settings.py

- Adjust settings in the file ``settings.py``.
- Install a cronjob that calls cron.sh with the path to the hostings, e.g.:

  ``30 12 * * 6 /opt/freewvs/cron.sh /path/to/hostings >> /var/log/hostingVulnScan 2>&1``


EXTENSION
=========
This tool is an addon to freewvs to adjust settings and generate a
csv-report. The sourcecode is written in python and does not modify the
original freewvs code.

Update
~~~~~~
The internal database is a set of ini-files with informations about scripts
and versions. The database is located in the directory ``freewvsdb``.
This directory will be automatically updated from schokokeks before the
cronjob starts the scan.

processResults.py
~~~~~~~~~~~~~~~~~
- This script parse the XML and generates an CSV report.
- Generates an e-mail with the CSV report.
- Send the e-mail to the referred persons.

settings.py
~~~~~~~~~~~
This file contains the configuration for ``processResults.py``.


DEBUGGING
=========
``Notice: freewvsdb updater is not working. This should be fixed!``
This means that the internal database is not proper updated.
The sequence is the following:

- ``cron.sh`` updates the ``freewvsdb`` directory with ``svn co``.
- scanning for vulnerability
- ``processResult.py`` will be started with the output of svn checkout as
  argument.
- check if an update is made and search for the database revision.


LICENSE
=======
Freewvs was developed by the german hosting provider Schokokeks and is open
source under the terms of creative commons CC0 1.0 Universal. The source
code is provided in a `svn repository`_.


.. _svn repository: https://svn.schokokeks.org/repos/freewvs/

.. vim: set spell spelllang=en sw=2 ts=2 et wrap tw=76 :
