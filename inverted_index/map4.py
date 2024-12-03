#!/usr/bin/env -S python3 -u
"""Map 3: Calculate Everything Else."""

import sys


def main():
    """Split input and transform."""
    for line in sys.stdin:
        # Strip whitespace and check for empty or malformed lines
        line = line.strip()
        if not line:
            continue

        try:
            # Split the input line into parts
            doc_id, rest = line.split("\t")
            term, tf_idf, tf_ik = rest.split()

            print(f"{doc_id}\t{term} {tf_idf} {tf_ik}")

        except ValueError:
            # Handle unexpected line formats (optional)
            print(f"Skipping malformed line: {line}", file=sys.stderr)


if __name__ == "__main__":
    main()
