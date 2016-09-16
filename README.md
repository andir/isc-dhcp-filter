# ISC DHCP Leases Filter Library for Python

[![BuildStatus](https://travis-ci.org/andir/isc-dhcp-filter.svg)](https://travis-ci.org/andir/isc-dhcp-filter)
[![Test Coverage](https://codeclimate.com/github/andir/isc-dhcp-filter/badges/coverage.svg)](https://codeclimate.com/github/andir/isc-dhcp-filter/coverage)
[![Issue Count](https://codeclimate.com/github/andir/isc-dhcp-filter/badges/issue_count.svg)](https://codeclimate.com/github/andir/isc-dhcp-filter)

This library provides a filter API on top of  [python-isc-dhcp-leases](https://github.com/MartijnBraam/python-isc-dhcp-leases).

The goal is to make parsing ISC DHCP Leases files less repetitive. Leases are parsed once and then only filtered during runtime. In the underlying library actions such as `.current` and `.active` would involve parsing the leases file for each call. Since parsing of larger files is rather slow caching of the raw `Lease` objects is desirable. This is what this library implements.

By storing the original leases and passing generators around the leases files only have to be parsed once.

## Features

* re-use parsed leases for usage with multiple filters
* Chainability of filters (`leases.active.v4.where_eq('foo', 'bar')`)
* `.v4` and `.v6` filter which filter by address family
* `.filter(lambda lease: lease.active == True)` to implement custom filters
* `.where_eq(key[, value])` filter by `set` key/value
* `.valid`, `.invalid`, `.active`, `.inactive` filters which use the corresponding lease attributes
* `.count()` returns the amount of leases


## Installation

`pip install isc-dhcp-filter`
