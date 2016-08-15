from setuptools import setup

setup(
    name="isc-dhcp-filter",
    version="0.0.1",
    description='This library provides a filter API on top of  python-isc-dhcp-leases.',
    install_requires=[
        "isc_dhcp_leases",
    ],
    tests_require=['freezegun'],
    packages=['isc_dhcp_filter'],
    test_suite='tests',
    author='Andreas Rammhold',
    author_email='andreas@rammhold.de',
    license='MIT'
)