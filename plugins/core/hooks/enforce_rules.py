#!/usr/bin/env python3
"""Self-contained hookify rule enforcer for core plugin.

Reads hookify.*.md files from the plugin root, parses frontmatter,
and enforces block/warn rules on PreToolUse and UserPromptSubmit events.
"""

import glob
import json
import os
import re
import sys

PLUGIN_ROOT = os.environ.get(
    "CLAUDE_PLUGIN_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

EVENT_FIELD = {"bash": "command", "file": "new_string", "prompt": "user_prompt"}


def parse_rule(filepath):
    """Parse a hookify.*.md file into a rule dict, or None if invalid/disabled."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return None

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    # Minimal YAML parser (stdlib only, handles simple key: value lines)
    frontmatter = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            value = value.strip().strip("\"'")
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            frontmatter[key.strip()] = value

    if frontmatter.get("enabled") is False:
        return None

    return {
        "name": frontmatter.get("name", "unnamed"),
        "event": frontmatter.get("event", "all"),
        "pattern": frontmatter.get("pattern"),
        "action": frontmatter.get("action", "warn"),
        "message": parts[2].strip(),
    }


def detect_event(input_data):
    """Determine event type from hook input."""
    tool_name = input_data.get("tool_name", "")
    if tool_name == "Bash":
        return "bash"
    if tool_name in ("Edit", "Write", "MultiEdit"):
        return "file"
    if "user_prompt" in input_data:
        return "prompt"
    return None


def extract_content(event, input_data):
    """Extract matchable text from hook input."""
    if event == "prompt":
        return input_data.get("user_prompt", "")

    tool_input = input_data.get("tool_input", {})
    field = EVENT_FIELD.get(event, "")
    if field and field in tool_input:
        return tool_input[field]

    # Fallback for file events
    if event == "file":
        return tool_input.get("content", "") or tool_input.get("new_string", "")
    return tool_input.get("command", "")


def main():
    try:
        input_data = json.load(sys.stdin)
        event = detect_event(input_data)
        if event is None:
            print("{}")
            sys.exit(0)

        # Load and filter rules
        rule_files = glob.glob(os.path.join(PLUGIN_ROOT, "hookify.*.md"))
        rules = []
        for path in rule_files:
            rule = parse_rule(path)
            if rule and rule["pattern"] and rule["event"] in (event, "all"):
                rules.append(rule)

        content = extract_content(event, input_data)
        if not content:
            print("{}")
            sys.exit(0)

        # Evaluate: accumulate all matches, blocking takes priority
        blocking = []
        warnings = []
        for rule in rules:
            try:
                if re.search(rule["pattern"], content):
                    if rule["action"] == "block":
                        blocking.append(rule)
                    else:
                        warnings.append(rule)
            except re.error:
                continue

        if blocking:
            msgs = [f"**[{r['name']}]**\n{r['message']}" for r in blocking]
            combined = "\n\n".join(msgs)
            hook_event = input_data.get("hook_event_name", "PreToolUse")
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": hook_event,
                            "permissionDecision": "deny",
                        },
                        "systemMessage": combined,
                    }
                )
            )
        elif warnings:
            msgs = [f"**[{r['name']}]**\n{r['message']}" for r in warnings]
            print(json.dumps({"systemMessage": "\n\n".join(msgs)}))
        else:
            print("{}")

    except Exception:
        print("{}")

    sys.exit(0)


if __name__ == "__main__":
    main()
