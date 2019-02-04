from setuptools import setup
from setuptools import find_packages


version = '0.0.1'

install_requires = [
    'acme>=0.21.1',
    'certbot>=0.21.1',
    'mock',
    'setuptools',
    'zope.interface',
]

setup(
    name='certbot-dns-cfproxy',
    version=version,
    description="Cloudflare Proxy DNS Authenticator plugin for Certbot",
    url='https://github.com/ProfFan/certbot-dns-cfproxy',
    author="Fan Jiang",
    author_email='i@fanjiang.me',
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-cfproxy = certbot_dns_cfproxy.dns_cfproxy:Authenticator',
        ],
    },
    test_suite='certbot_dns_cfproxy',
)
