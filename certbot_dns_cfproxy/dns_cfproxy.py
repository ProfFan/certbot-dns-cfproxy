"""DNS Authenticator for Cloudflare Proxy."""
import logging

import requests
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://www.cloudflare.com/a/account/my-account'


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for CFProxy

    This Authenticator uses the CFProxy API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are using CFProxy for '
                   'DNS).')
    ttl = 120

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='CFProxy credentials INI file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the CFProxy API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'CFProxy credentials INI file',
            {
                'user': 'user address associated with CFProxy account',
                'api-key': 'API key for CFProxy account, obtained from {0}'.format(ACCOUNT_URL),
                'api-endpoint': 'API endpoint URL'
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_cloudflare_client().add_txt_record(domain, validation_name, validation, self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        self._get_cloudflare_client().del_txt_record(domain, validation_name, validation)

    def _get_cloudflare_client(self):
        return _CFProxyClient(self.credentials.conf('user'),
                                 self.credentials.conf('api-key'),
                                 self.credentials.conf('api-endpoint'))


class _CFProxyClient(object):
    """
    Encapsulates all communication with the CFProxy API.
    """

    def __init__(self, user, api_key, api_endpoint):
        self.user = user
        self.key = api_key
        self.api_ep = api_endpoint

    def add_txt_record(self, domain, record_name, record_content, record_ttl):
        """
        Add a TXT record using the supplied information.

        :param str domain: The domain to use to look up the CFProxy zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the CFProxy API
        """

        zone_alts = dns_common.base_domain_name_guesses(domain)

        for alt in zone_alts:
            data = {'rectype': 'TXT',
                    'zone': alt,
                    'rec': record_name,
                    'value': record_content,
                    'ttl': record_ttl,
                    'user': self.user,
                    'key': self.key}

            try:
                logger.debug('Attempting to add record to zone %s: %s', domain, data)
                r = requests.post(self.api_ep + "/add", json=data)
                if r.json()['success']:
                    return
            except requests.exceptions.RequestException as e:
                logger.error('Encountered Error adding TXT record: %d %s', e, e)
                raise errors.PluginError('Error communicating with the CFProxy API: {0}'.format(e))

    def del_txt_record(self, domain, record_name, record_content):
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain: The domain to use to look up the CFProxy zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """
        zone_alts = dns_common.base_domain_name_guesses(domain)

        for alt in zone_alts:
            data = {'rectype': 'TXT',
                    'zone': alt,
                    'rec': record_name,
                    'value': record_content,
                    'user': self.user,
                    'key': self.key}

            try:
                logger.debug('Attempting to add record to zone %s: %s', domain, data)
                r = requests.post(self.api_ep + "/delete", json=data)
                if r.json()['success']:
                    return
            except requests.exceptions.RequestException as e:
                logger.error('Encountered Error adding TXT record: %d %s', e, e)
                raise errors.PluginError('Error communicating with the CFProxy API: {0}'.format(e))

