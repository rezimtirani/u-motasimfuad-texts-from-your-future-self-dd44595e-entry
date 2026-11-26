"""Texts From Your Future Self — make.fun entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt: a text message from
the writer's future self, ten years on, with a warning about the
unread courses, the unfinished project, the thirsty plant, and the
password that never changed. Only the Python standard library is used.
"""

import os
import sys

FUTURE_TEXT = "It's me, you from 2036. Delete the 47 unread courses, start the project today, and water the plant — future you is still waiting on that one. P.S. The password is still hunter2."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def validate_text(text):
    """Return the text once it passes the sealed gate, else raise.

    The gate counts UTF-8 characters, not bytes, so the line must be a
    single line of 1 to 200 characters, not only whitespace, with no
    trailing newline and no control characters in the output file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, over the {MAX_CHARS} gate")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def describe_text(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so a line with wide
    characters reads shorter than its byte length; an ASCII line reads
    the same either way. Returns a one-line human-readable summary.
    """
    chars = len(text)
    byte_count = len(text.encode("utf-8"))
    word_count = len(text.split())
    return f"{chars} characters, {byte_count} UTF-8 bytes, {word_count} words"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        raise SystemExit(1)
    line = validate_text(FUTURE_TEXT)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {os.path.join(out_dir, 'entry.txt')} ({describe_text(line)})")


if __name__ == "__main__":
    main()
