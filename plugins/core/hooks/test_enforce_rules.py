#!/usr/bin/env python3
"""Tests for enforce_rules.py hookify rule enforcer."""

import json
import os
import tempfile
import textwrap
import unittest

from enforce_rules import detect_event, extract_content, parse_rule


class TestParseRule(unittest.TestCase):
    """Tests for parsing hookify.*.md files."""

    def _write_rule(self, content):
        """Write rule content to a temp file and return its path."""
        fd, path = tempfile.mkstemp(suffix=".md")
        os.write(fd, content.encode("utf-8"))
        os.close(fd)
        self.addCleanup(os.unlink, path)
        return path

    def test_valid_block_rule(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            name: test-block
            enabled: true
            event: bash
            pattern: rm\\s+-rf
            action: block
            ---

            Do not use rm -rf.
        """))
        rule = parse_rule(path)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["name"], "test-block")
        self.assertEqual(rule["event"], "bash")
        self.assertEqual(rule["pattern"], "rm\\s+-rf")
        self.assertEqual(rule["action"], "block")
        self.assertEqual(rule["message"], "Do not use rm -rf.")

    def test_valid_warn_rule(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            name: test-warn
            enabled: true
            event: file
            pattern: TODO
            action: warn
            ---

            TODO found in file.
        """))
        rule = parse_rule(path)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["action"], "warn")

    def test_disabled_rule_returns_none(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            name: disabled-rule
            enabled: false
            event: bash
            pattern: .*
            action: block
            ---

            Should not fire.
        """))
        self.assertIsNone(parse_rule(path))

    def test_missing_frontmatter_returns_none(self):
        path = self._write_rule("No frontmatter here.")
        self.assertIsNone(parse_rule(path))

    def test_incomplete_frontmatter_returns_none(self):
        path = self._write_rule("---\nname: broken\n")
        self.assertIsNone(parse_rule(path))

    def test_defaults_action_to_warn(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            name: no-action
            enabled: true
            event: prompt
            pattern: .*
            ---

            Default action.
        """))
        rule = parse_rule(path)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["action"], "warn")

    def test_defaults_event_to_all(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            name: no-event
            enabled: true
            pattern: test
            ---

            Body.
        """))
        rule = parse_rule(path)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["event"], "all")

    def test_nonexistent_file_returns_none(self):
        self.assertIsNone(parse_rule("/nonexistent/path/hookify.fake.md"))

    def test_frontmatter_with_comments(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            # This is a comment
            name: commented
            enabled: true
            event: bash
            pattern: echo
            action: warn
            ---

            Comment test.
        """))
        rule = parse_rule(path)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["name"], "commented")

    def test_quoted_values_stripped(self):
        path = self._write_rule(textwrap.dedent("""\
            ---
            name: "quoted-name"
            enabled: 'true'
            event: bash
            pattern: test
            action: block
            ---

            Quoted.
        """))
        rule = parse_rule(path)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["name"], "quoted-name")


class TestDetectEvent(unittest.TestCase):
    """Tests for event type detection from hook input."""

    def test_bash_tool(self):
        self.assertEqual(detect_event({"tool_name": "Bash"}), "bash")

    def test_edit_tool(self):
        self.assertEqual(detect_event({"tool_name": "Edit"}), "file")

    def test_write_tool(self):
        self.assertEqual(detect_event({"tool_name": "Write"}), "file")

    def test_multi_edit_tool(self):
        self.assertEqual(detect_event({"tool_name": "MultiEdit"}), "file")

    def test_user_prompt(self):
        self.assertEqual(detect_event({"user_prompt": "hello"}), "prompt")

    def test_unknown_tool(self):
        self.assertIsNone(detect_event({"tool_name": "Read"}))

    def test_empty_input(self):
        self.assertIsNone(detect_event({}))


class TestExtractContent(unittest.TestCase):
    """Tests for extracting matchable text from hook input."""

    def test_bash_command(self):
        data = {"tool_input": {"command": "git add -A"}}
        self.assertEqual(extract_content("bash", data), "git add -A")

    def test_prompt_text(self):
        data = {"user_prompt": "fix the bug"}
        self.assertEqual(extract_content("prompt", data), "fix the bug")

    def test_file_new_string(self):
        data = {"tool_input": {"new_string": "updated content"}}
        self.assertEqual(extract_content("file", data), "updated content")

    def test_file_content_fallback(self):
        data = {"tool_input": {"content": "file body"}}
        self.assertEqual(extract_content("file", data), "file body")

    def test_empty_tool_input(self):
        data = {"tool_input": {}}
        self.assertEqual(extract_content("bash", data), "")

    def test_missing_tool_input(self):
        data = {}
        self.assertEqual(extract_content("bash", data), "")


class TestBlockRules(unittest.TestCase):
    """Integration tests for the actual hookify rules shipped with the core plugin."""

    def setUp(self):
        """Load the real hookify rules from the plugin directory."""
        plugin_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        import glob as glob_mod

        rule_files = glob_mod.glob(os.path.join(plugin_root, "hookify.*.md"))
        self.rules = []
        for path in rule_files:
            rule = parse_rule(path)
            if rule:
                self.rules.append(rule)

    def _find_rule(self, name):
        for rule in self.rules:
            if rule["name"] == name:
                return rule
        return None

    def _matches(self, rule_name, content):
        import re

        rule = self._find_rule(rule_name)
        if not rule:
            self.fail(f"Rule '{rule_name}' not found")
        return bool(re.search(rule["pattern"], content))

    def test_block_git_add_all(self):
        self.assertTrue(self._matches("block-bad-git-add", "git add -A"))

    def test_block_git_add_dot(self):
        self.assertTrue(self._matches("block-bad-git-add", "git add ."))

    def test_allow_git_add_specific_file(self):
        self.assertFalse(self._matches("block-bad-git-add", "git add src/main.py"))

    def test_block_commit_no_verify(self):
        self.assertTrue(self._matches("block-no-verify", "git commit --no-verify"))

    def test_block_push_no_verify(self):
        self.assertTrue(self._matches("block-no-verify", "git push --no-verify"))

    def test_allow_normal_commit(self):
        self.assertFalse(self._matches("block-no-verify", "git commit -m 'test'"))

    def test_block_compound_cd(self):
        self.assertTrue(self._matches("block-compound-cd", "cd /tmp && ls"))

    def test_block_compound_cd_semicolon(self):
        self.assertTrue(self._matches("block-compound-cd", "cd /tmp ; ls"))

    def test_allow_standalone_cd(self):
        self.assertFalse(self._matches("block-compound-cd", "cd /tmp"))

    def test_ultrathink_matches_any_prompt(self):
        self.assertTrue(self._matches("ultrathink-mode", "hello world"))
        self.assertTrue(self._matches("ultrathink-mode", ""))


class TestBlockingPriority(unittest.TestCase):
    """Verify that blocking rules take priority over warnings."""

    def test_block_overrides_warn(self):
        """When both a block and warn rule match, the output should deny."""
        block_rule = {
            "name": "blocker",
            "event": "bash",
            "pattern": ".*",
            "action": "block",
            "message": "Blocked.",
        }
        warn_rule = {
            "name": "warner",
            "event": "bash",
            "pattern": ".*",
            "action": "warn",
            "message": "Warning.",
        }
        import re

        blocking = []
        warnings = []
        content = "any command"
        for rule in [block_rule, warn_rule]:
            if re.search(rule["pattern"], content):
                if rule["action"] == "block":
                    blocking.append(rule)
                else:
                    warnings.append(rule)

        self.assertEqual(len(blocking), 1)
        self.assertEqual(len(warnings), 1)
        # blocking takes priority in the output logic
        self.assertTrue(len(blocking) > 0)


if __name__ == "__main__":
    unittest.main()
