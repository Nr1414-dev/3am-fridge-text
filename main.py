#!/usr/bin/env python3
"""The 3AM Fridge Text — make.fun bounty entry.

Writes the one-line fridge text to /output/entry.txt.
Deterministic: the same bytes on every run, no randomness, no I/O
besides the single output file.
"""

import os

ENTRY = "3am. u up? It's the fridge. The light is on, the cheese is awake, and you already know why you're here."
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 140


def validate(text):
    """Enforce the bounty gate: UTF-8 text of 1 to 140 characters,
    a single line, not only whitespace."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to 140 characters, got %d" % len(text))
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")
    return text


def main():
    text = validate(ENTRY)
    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(OUTPUT_PATH, 0o644)
    # Read-back guard: the bytes on disk must be byte-identical to the
    # validated entry; fail loudly instead of shipping a wrong file.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise RuntimeError("read-back mismatch: disk bytes differ from entry")
    print("wrote %d bytes to %s" % (len(written), OUTPUT_PATH))


if __name__ == "__main__":
    main()
