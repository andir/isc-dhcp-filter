from isc_dhcp_leases import IscDhcpLeases
from isc_dhcp_leases import Lease
from isc_dhcp_leases import Lease6


def parse(*files):
    parsed_files = list(map(lambda file: IscDhcpLeases(file).get(), files))
    return Leases(*parsed_files)


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
        :param filter_func: function that returns true for all
                            values that should be accepted
        :return:
        """
        g = (l for l in self if filter_func(l))
        return Leases(g)

    def where_eq(self, key, value=None):
        """
        Filter leases by supplied set-key and value (if provided)
        :param key: the key in the sets dictionary of the lease
        :param value: the value for the supplied key, if None any lease
                      with the key is returned
        :return:
        """
        if value:
            def filter_func(lease):
                return lease.sets.get(key, None) == value
        else:
            def filter_func(lease):
                return key in lease.sets

        g = filter(filter_func, self)

        return Leases(g)

    def count(self):
        """
        Returns the count of leases in the current set of leases
        :return: int count of leases
        """
        return len(self)

    def __iter__(self):
        """
        Returns an iterator for the current set of leases
        :return:
        """
        if self._leases:
            yield from iter(self._leases)
        elif self._iter:
            yield from self._iter()

    def __len__(self):
        """
        Implements __len__
        If we are dealing with a generator we will expand it into `_leases`
        :return:
        """
        if type(self._leases) is list:
            return len(self._leases)
        else:
            l = list(iter(self))
            self._leases = l
            return len(l)
