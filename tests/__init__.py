import os
from unittest import TestCase

from isc_dhcp_leases import Lease
from isc_dhcp_leases.iscdhcpleases import BaseLease

from isc_dhcp_filter import parse, Leases
from freezegun import freeze_time


class LeaseLoaderMixin:
    @classmethod
    def setUpClass(cls):
        cls._basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

    def setUp(self):
        self.leases = parse(os.path.join(self._basepath, self.filename))
        super(LeaseLoaderMixin, self).setUp()


class BaseLeaseTester:
    def test_active_valid_current(self):
        active_valid = list(self.leases.active.valid)
        valid_active = list(self.leases.valid.active)

        self.assertEqual(len(active_valid), len(valid_active))
        self.assertEqual(len(active_valid), len(list(self.leases.current)))

    def test_v4_filter(self):
        for lease in self.leases.v4:
            self.assertIsInstance(lease, Lease)

    def test_v6_filter(self):
        for lease in self.leases.v4:
            self.assertIsInstance(lease, Lease)

    def test_valid_filter(self):
        for lease in self.leases.valid:
            self.assert_(lease.valid)

    def test_invalid_filter(self):
        for lease in self.leases.invalid:
            self.assert_(not lease.valid)

    def test_active_filter(self):
        for lease in self.leases.active:
            self.assert_(lease.active)

    def test_inactive_filter(self):
        for lease in self.leases.inactive:
            self.assert_(not lease.active)

    def test_current_filter(self):
        for lease in self.leases.current:
            self.assert_(lease.active)
            self.assert_(lease.current)

    def test_filter_func(self):
        l = list(self.leases.filter(lambda x: False))
        self.assertEqual(l, [])

        l = list(self.leases.filter(lambda x: isinstance(x, BaseLease)))
        self.assertEqual(l, list(self.leases))

    def test_filter_combine(self):
        combined = Leases(self.leases.v4, self.leases.v6)
        l = len(list(combined))
        self.assertGreater(l, 0)
        self.assertEqual(l, len(list(self.leases)))


class TestDhcpd6(LeaseLoaderMixin, BaseLeaseTester, TestCase):
    filename = 'dhcpd6-4.3.3.leases'

    def test_dhcpv6_active(self):
        leases = self.leases

        self.assertEqual(len(list(leases)), 4)
        self.assertEqual(len(list(leases.active)), 4)

    @freeze_time("2015-07-6 8:15:0")
    def test_dhcpv6_active_valid(self):
        leases = self.leases

        active_valid = list(leases.active.valid)
        valid_active = list(leases.valid.active)

        self.assertEqual(len(active_valid), len(valid_active))
        self.assertEqual(len(active_valid), len(list(leases.current)))

    def test_dhcpv6_invalid(self):
        leases = self.leases

        self.assertEqual(list(leases.invalid), list(leases))
        self.assertEqual(len(list(leases)), 4)

    def test_where_eq(self):
        leases = self.leases.where_eq('iana')
        self.assertEqual(len(list(leases)), 2)

        leases = self.leases.where_eq('iana', '2001:10:30:0:0:0:0:1fe')
        self.assertEqual(len(list(leases)), 1)

        leases = self.leases.where_eq('clientduid', '0100011cf710a5002722332b34')
        self.assertEqual(len(list(leases)), 2)

        leases = self.leases.where_eq('clientduid')
        self.assertEqual(len(list(leases)), 4)


class TestDebian7(LeaseLoaderMixin, BaseLeaseTester, TestCase):
    filename = 'debian7.leases'

    def test_vendor_class_identifier(self):
        leases1 = list(self.leases.where_eq('vendor-class-identifier'))
        leases2 = list(self.leases.where_eq('vendor-class-identifier', 'Some Vendor Identifier'))
        self.assertEqual(leases1, leases2)