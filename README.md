# certbot-dns-cfproxy

Install with `python setup.py install`.

Create the credentials file with:

```ini
certbot_dns_cfproxy:dns_cfproxy_user = fan
certbot_dns_cfproxy:dns_cfproxy_api_key = fp9ahf98sa8hfq29h
certbot_dns_cfproxy:dns_cfproxy_api_endpoint = http://your.cfproxy.api:8808
```

and get your cert with

```bash
certbot certonly \\
     -a certbot-dns-cfproxy:dns-cfproxy \\
     -d example.com
```

# LICENSE

Apache