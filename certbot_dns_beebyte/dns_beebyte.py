"""DNS Authenticator for beebyte.se."""
import logging

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

import requests

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for beebyte.se
    This Authenticator uses the portal.beebyte.se DNS API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using beebyte.se for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=5
        )
        add("credentials", help="beebyte.se credentials INI file.")
        add("wait", help="Wait for DNS change to happen.", action="store_true")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the portal.beebyte.se DNS API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "beebyte.se credentials INI file",
            {
                "api_key": "API KEY.",
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_beebyte_client().add_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_beebyte_client().del_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _get_beebyte_client(self):
        return _BeebyteClient(
            self.credentials.conf("api_key"),
            self.conf("wait"),
        )


class _BeebyteClient(object):
    def __init__(self, api_key, wait):
        logger.debug("creating beebyte API client")
        self.api_key = api_key
        self.wait = wait

    def add_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Add a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the beebyte API
        """
        url = 'https://portal.beebyte.se/api/v1/domain/%s/dns01/' % (domain)
        data = {
            'record_name': record_name,
            'record_content': record_content,
            'wait': self.wait,
        }
        headers = {'DNS-01-API-KEY': self.api_key}
        req = requests.post(url, json=data, headers=headers)


    def del_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Delete a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the beebyte API
        """
        url = 'https://portal.beebyte.se/api/v1/domain/%s/dns01/' % (domain)
        data = {
            'record_name': record_name,
            'record_content': record_content,
            'wait': self.wait,
        }
        headers = {'DNS-01-API-KEY': self.api_key}
        req = requests.delete(url, json=data, headers=headers)
