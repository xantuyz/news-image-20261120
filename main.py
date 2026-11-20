#!/usr/bin/env python3
"""Hand the finished front page to the grading harness.

render.py draws entry.png with Pillow; this entrypoint needs only the
standard library, so it runs in the sandbox with nothing installed.
It places a copy of entry.png at $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png) and refuses to report success unless
the copy's SHA-256 matches the original byte for byte.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as handle:
        image = handle.read()
    with open(target, "wb") as handle:
        handle.write(image)
    with open(target, "rb") as handle:
        written = handle.read()
    if digest(image) != digest(written):
        sys.stderr.write("entry.png copy failed its digest check\n")
        return 1
    sys.stdout.write("wrote %s (%d bytes, sha256 %s)\n"
                     % (target, len(written), digest(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
