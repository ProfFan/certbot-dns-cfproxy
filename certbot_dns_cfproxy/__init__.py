"""
The `~certbot_dns_cfproxy.dns_cfproxy` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the CFProxy API.

Examples
--------

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``

   certbot certonly \\
     -a certbot-dns-cfproxy:dns-cfproxy \\
     -d example.com

"""
