"""Extract PreForm's MSI from the WiX Burn bundle without running Windows code."""

import mmap
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def extract(installer, destination):
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        with open(installer, "rb") as source, mmap.mmap(
            source.fileno(), 0, access=mmap.ACCESS_READ
        ) as data:
            cabinets = []
            offset = 0
            while (offset := data.find(b"MSCF\0\0\0\0", offset)) != -1:
                size = struct.unpack_from("<I", data, offset + 8)[0]
                if size >= 36 and offset + size <= len(data):
                    cabinet = directory / f"{offset}.cab"
                    cabinet.write_bytes(data[offset : offset + size])
                    cabinets.append(cabinet)
                offset += 8
        if len(cabinets) != 2:
            raise ValueError("Expected the two cabinets in the PreForm 3.64.1 bundle")
        # WiX stores its manifest in file '0' in the first (bootstrapper) CAB.
        subprocess.run(
            ["cabextract", "-q", "-F", "0", "-d", str(directory), str(cabinets[0])],
            check=True,
        )
        manifest = ET.parse(directory / "0")
        ns = {"w": "http://schemas.microsoft.com/wix/2008/Burn"}
        payload = next(
            item for item in manifest.findall("w:Payload", ns)
            if item.get("FilePath") == "PreForm_setup.msi"
        )
        name = payload.attrib["SourcePath"]
        if Path(name).name != name or name in (".", ".."):
            raise ValueError("Invalid payload filename")
        subprocess.run(
            ["cabextract", "-q", "-F", name, "-d", str(directory), str(cabinets[1])],
            check=True,
        )
        package = (directory / name).read_bytes()
        if len(package) != int(payload.attrib["FileSize"]):
            raise ValueError("Incorrect MSI payload size")
        if not package.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
            raise ValueError("Payload is not an MSI compound document")
        Path(destination).write_bytes(package)


if __name__ == "__main__":
    extract(*sys.argv[1:])
