"""Route PreForm 3.65.0.671's DNS imports through a compatibility DLL."""

import hashlib
from pathlib import Path
import sys


# Revalidate the DNS imports and update this hash when upgrading PreForm.
# The compatibility DLL supports DnsFree, DnsStartMulticastQuery, and
# DnsStopMulticastQuery.
EXPECTED_SHA256 = '8ab42f58d33b9e70f9a1dc18163b42b9a80c5a24e67e22a9581d8a7cc9370f51'


def patch(path):
    path = Path(path)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Expected the unmodified PreForm 3.65.0.671 executable')

    original = b'DNSAPI.dll\0'
    replacement = b'pf-dns.dll\0'
    if data.count(original) != 1:
        raise ValueError('Expected exactly one DNSAPI.dll name')
    # Same-length replacement preserves the PE layout and all other imports.
    path.write_bytes(data.replace(original, replacement))


if __name__ == '__main__':
    patch(sys.argv[1])
