"""Route PreForm 3.65.1.672's DNS imports through a compatibility DLL."""

import hashlib
from pathlib import Path
import sys


# Revalidate the DNS imports and update this hash when upgrading PreForm.
# The compatibility DLL supports DnsFree, DnsStartMulticastQuery, and
# DnsStopMulticastQuery.
EXPECTED_SHA256 = '1fb4e7b7cec05250154ab9493f0daf07a04cec08c022a0d4c172d8a846f25ff5'


def patch(path):
    path = Path(path)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Expected the unmodified PreForm 3.65.1.672 executable')

    original = b'DNSAPI.dll\0'
    replacement = b'pf-dns.dll\0'
    if data.count(original) != 1:
        raise ValueError('Expected exactly one DNSAPI.dll name')
    # Same-length replacement preserves the PE layout and all other imports.
    path.write_bytes(data.replace(original, replacement))


if __name__ == '__main__':
    patch(sys.argv[1])
