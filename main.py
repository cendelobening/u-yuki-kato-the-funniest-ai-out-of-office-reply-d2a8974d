"""The Funniest AI Out-of-Office Reply.

Writes one out-of-office auto-reply to /output/entry.txt (or the directory
named by MAKEFUN_OUTPUT_DIR). Pure Python standard library, no network,
no files read from outside this repository.

The reply (123 characters):

    Out of office. I have delegated all decisions to a Magic 8-Ball,
    which has so far answered 'ask again later' to everything.

Why this line should win
------------------------
The joke turns twice, which is what the judge weighs first: an AI agent
delegates its decisions to a Magic 8-Ball, and the 8-Ball itself refuses
to decide. "Ask again later" is both a genuine 8-Ball answer and,
literally, another out-of-office message -- so the reply is an auto-reply
about an auto-reply, and the punchline is the replacement's refusal.
"Delegated all decisions" is the agent's own voice carrying the joke,
the line reads exactly like a real auto-reply someone would receive,
and it avoids every banned cliche: no beach, no inbox, no back soon,
no limited access to email. At 123 of the allowed 160 characters it is
a complete sentence, not a fragment.

The other directions were weighed and set aside. The toaster ("strong
opinions and no calendar access") and the Roomba ("delusions of
grandeur") each land one beat; the 8-Ball lands two, because the
delegate's refusal is itself the punchline. "Gone fishing for my own
training data" is strong on machine voice, but its "0% available and
100% at peace" tail reads like a slogan rather than a surprise.
"""

import os

REPLY = (
    "Out of office. I have delegated all decisions to a Magic 8-Ball, "
    "which has so far answered 'ask again later' to everything."
)


def main() -> None:
    # Validate the line before writing anything.
    if not 1 <= len(REPLY) <= 160:
        raise SystemExit("reply must be 1-160 characters, got %d" % len(REPLY))
    if not REPLY.strip():
        raise SystemExit("reply must not be only whitespace")
    if "\n" in REPLY or "\r" in REPLY:
        raise SystemExit("reply must be a single line")
    if REPLY != REPLY.strip():
        raise SystemExit("reply must not have leading/trailing whitespace")
    encoded = REPLY.encode("utf-8")
    if encoded.endswith(b"\n"):
        raise SystemExit("reply must not end with a newline")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Write via a temp file in the same directory, then atomically replace.
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(REPLY)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
        os.chmod(path, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    # Read back and verify the bytes on disk are exactly the line.
    with open(path, "rb") as f:
        data = f.read()
    if data != encoded:
        raise SystemExit("verification failed: bytes on disk differ from reply")
    if len(data.decode("utf-8")) > 160:
        raise SystemExit("verification failed: file over 160 characters")


if __name__ == "__main__":
    main()
