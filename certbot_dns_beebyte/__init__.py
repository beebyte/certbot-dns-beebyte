"""
The `~certbot_dns_beebyte.dns_beebyte` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the beebyte customer portal API.

Named Arguments
---------------
========================================  =====================================
``--dns-beebyte:credentials``             beebyte.se credentials_
                                          INI file. (Required)
========================================  =====================================


Credentials
-----------

.. code-block:: ini
   :name: credentials.ini
   :caption: Example credentials file:
   # beebyte.se credentials used by Certbot
   dns_beebyte_api_key = keykeykey


The path to this file can be provided interactively or using the
``--dns-beebyte-credentials`` command-line argument. Certbot records the path
to this file for use during renewal, but does not store the file's contents.
"""
