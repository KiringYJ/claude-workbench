#!/usr/bin/env python3
"""Pre-commit doc review hook.

Prompts Claude to review all project documentation before committing.
Runs as a Claude PreToolUse hook on git commit/push/pr create.
"""

import json
import re
import sys


def main():
    try:
        if sys.stdin.isatty():
            print("This script runs as a Claude PreToolUse hook.", file=sys.stderr)
            sys.exit(1)

        input_data = json.load(sys.stdin)
        command = input_data.get("tool_input", {}).get("command", "")
        is_commit = bool(re.match(r"git\s+commit(\s|$)", command.strip()))
        is_push = bool(re.match(r"git\s+push(\s|$)", command.strip()))
        is_pr = bool(re.match(r"gh\s+pr\s+create(\s|$)", command.strip()))

        if not (is_commit or is_push or is_pr):
            print("{}")
            sys.exit(0)

        print(
            json.dumps(
                {
                    "systemMessage": (
                        "Before committing, review ALL project documentation "
                        "(README.md, CLAUDE.md, etc.) to ensure it accurately "
                        "reflects the current changes — including descriptions, "
                        "usage instructions, file structure, and any other "
                        "content. Read each doc file and verify."
                    )
                }
            )
        )
    except (json.JSONDecodeError, KeyError, OSError):
        print("{}")

    sys.exit(0)


if __name__ == "__main__":
    main()
