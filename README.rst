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


LICENSE
=======
Freewvs was developed by the german hosting provider Schokokeks and is open
source under the terms of creative commons CC0 1.0 Universal. The source
code is provided in a `svn repository`_.


.. _svn repository: https://svn.schokokeks.org/repos/freewvs/

.. vim: set spell spelllang=en sw=2 ts=2 et wrap tw=76 :
