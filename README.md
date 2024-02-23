# certbot-dns-beebyte
Certbot Plugin to handle DNS-01 challenges for beebyte.se managed domains

Installation
------------

    pip install 'git+https://github.com/beebyte/certbot-dns-beebyte'

In case `certbot plugins` does not show the installed plugin, verify using `pip show certbot-dns-beebyte` where it was installed.

If it has been installed to `/usr/local/lib/python*/site-packages` certbot _might_ not find it. Either symlink to
`/usr/lib/python*/site-packages` or reinstall using the `--prefix` parameter:

    pip install --prefix=/usr 'git+https://github.com/beebyte/certbot-dns-beebyte'

Named Arguments
---------------

To start using DNS authentication for beebyte, pass the following arguments on certbot's command line:

Option|Description|
---|---|
`--authenticator dns-beebyte`|select the authenticator plugin (Required)|
`--dns-beebyte-credentials FILE`|beebyte credentials INI file. (Required)|
`--dns-beebyte-propagation-seconds NUM`|waiting time for DNS to propagate before asking the ACME server to verify the DNS record. (Default: 5, Recommended: \>= 10)|
`--dns-beebyte-wait`|wait until the change is actually	present	in DNS which has the benefit of not having to set a large propagation delay.

Credentials
-----------

Credentials are stored in an .ini file and referenced using the `--dns-beebyte-credentials` parameter.

    # beebyte credentials used by Certbot
    dns_beebyte_api_key = keykeykeykey

Usage
-----

    certbot -v \
        certonly \
        --authenticator dns-beebyte \
        --dns-beebyte-credentials /etc/certbot-dns-beebyte.ini \
        --dns-beebyte-wait \
        -d example.com
