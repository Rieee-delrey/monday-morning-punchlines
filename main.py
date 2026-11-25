#!/usr/bin/env python3
"""Monday Morning Punchlines entry: write the sim-winning one-liner to
/output/entry.txt and prove the file holds exactly that line.

The line is checked three times: in memory before the write, on the bytes
read back from disk after the write, and once more on a second read, so a
truncated or altered file can never pass silently. The entry gate allows
1 to 200 characters; this line is 59.
"""

import hashlib
import os

LINE = "I asked Monday for a day off. It took Tuesday as a hostage."

MAX_CHARS = 200
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")


def check_line(text):
    """Refuse anything that is not one clean line inside the gate."""
    if not isinstance(text, str) or not text:
        raise ValueError("line must be non-empty text")
    if len(text) > MAX_CHARS:
        raise ValueError("line is %d chars, over the %d-char limit" % (len(text), MAX_CHARS))
    if text != text.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    return text


def write_entry():
    check_line(LINE)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    with open(OUT_PATH, "rb") as handle:
        written = handle.read()
    if written != LINE.encode("utf-8"):
        raise ValueError("read-back mismatch: file does not hold the line")
    with open(OUT_PATH, encoding="utf-8") as handle:
        again = handle.read()
    if again != LINE:
        raise ValueError("second read mismatch")
    return written


def main():
    written = write_entry()
    digest = hashlib.sha256(written).hexdigest()
    print(LINE)
    print("wrote %d bytes to %s sha256=%s" % (len(written), OUT_PATH, digest))


if __name__ == "__main__":
    main()
