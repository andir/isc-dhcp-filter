from isc_dhcp_leases import Lease
from isc_dhcp_leases import Lease6
from isc_dhcp_leases import IscDhcpLeases


def parse(*files):
    return Leases(*[leases for leases in map(lambda file: IscDhcpLeases(file).get(), files)])


class Leases:
    _leases = []
    _iter = None

    def __init__(self, *args):
        l = len(args)
        if l > 1:
            # create a new iterator that can be called again
            def _iter():
                for argument in args:
                    yield from argument

            self._leases = None
            self._iter = _iter
        elif l == 1:
            self._leases = args[0]
        else:
            # fallback to empty list if there are no leases given
            self._leases = []

    @property
    def current(self):
        """
        Leases where the active and valid properties are True
        :return:
        """
        return self.active.valid

    @property
    def active(self):
        """
        Leases where the active property is True
        :return:
        """
        g = (l for l in self if l.active)
        return Leases(g)

    @property
    def inactive(self):
        """
        Leases where the active property is False
        :return:
        """
        g = (l for l in self if not l.active)
        return Leases(g)

    @property
    def valid(self):
        """
        Leases where the valid property is True
        :return:
        """
        g = (l for l in self if l.valid)
        return Leases(g)

    @property
    def invalid(self):
        """
        Leases where the valid property is False
        :return:
        """
        g = (l for l in self if not l.valid)
        return Leases(g)

    @property
    def v4(self):
        """
        Leases that are an instance of Lease
        :return:
        """
        g = (l for l in self if isinstance(l, Lease))
        return Leases(g)

    @property
    def v6(self):
        """
        Leases that are an instance of Lease6
        :return:
        """
        g = (l for l in self if isinstance(l, Lease6))
        return Leases(g)

    def filter(self, filter_func):
        """
        Filter leases by supplied filter function
        :param filter_func: function that returns true for all values that should be accepted
        :return:
        """
        g = (l for l in self if filter_func(l))
        return Leases(g)

    def where_eq(self, key, value=None):
        """
        Filter leases by supplied set-key and value (if provided)
        :param key: the key in the sets dictionary of the lease
        :param value: the value for the supplied key, if None any lease with the key is returned
        :return:
        """
        if value:
            g = (l for l in self if l.sets.get(key, None) == value)
        else:
            g = (l for l in self if key in l.sets)

        return Leases(g)

    def __iter__(self):
        """
        Returns an iterator for the current set of leases
        :return:
        """
        if self._leases:
            yield from iter(self._leases)
        elif self._iter:
            yield from self._iter()