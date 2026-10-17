"""Route PreForm 3.64.1.664's DNS imports through a compatibility DLL."""

import hashlib
from pathlib import Path
import sys


# Revalidate the DNS imports and update this hash when upgrading PreForm.
# The compatibility DLL supports DnsFree, DnsStartMulticastQuery, and
# DnsStopMulticastQuery.
EXPECTED_SHA256 = '074709c9b10e08f028b4c2f56f8022d246d954fa93ad80c1d5e680778bca4946'


def patch(path):
    path = Path(path)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Expected the unmodified PreForm 3.64.1.664 executable')

    original = b'DNSAPI.dll\0'
    replacement = b'pf-dns.dll\0'
    if data.count(original) != 1:
        raise ValueError('Expected exactly one DNSAPI.dll name')
    # Same-length replacement preserves the PE layout and all other imports.
    path.write_bytes(data.replace(original, replacement))


if __name__ == '__main__':
    patch(sys.argv[1])
