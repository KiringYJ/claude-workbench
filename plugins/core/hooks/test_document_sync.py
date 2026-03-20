#!/usr/bin/env python3
"""Tests for document_sync.py pre-commit doc review hook."""

import contextlib
import json
import unittest
from io import StringIO
from unittest.mock import patch

from document_sync import main


def _run_hook(input_data):
    """Run the hook main() with simulated stdin and capture stdout."""
    stdin_text = json.dumps(input_data)
    with (
        patch("sys.stdin", StringIO(stdin_text)),
        patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        patch("sys.exit", side_effect=SystemExit),
    ):
        with contextlib.suppress(SystemExit):
            main()
        return mock_stdout.getvalue()


class TestDocumentSync(unittest.TestCase):
    """Tests for document_sync.py hook behavior."""

    def test_git_commit_triggers_review(self):
        output = _run_hook({"tool_input": {"command": "git commit -m 'test'"}})
        result = json.loads(output)
        self.assertIn("systemMessage", result)
        self.assertIn("documentation", result["systemMessage"].lower())

    def test_git_push_triggers_review(self):
        output = _run_hook({"tool_input": {"command": "git push origin main"}})
        result = json.loads(output)
        self.assertIn("systemMessage", result)

    def test_gh_pr_create_triggers_review(self):
        output = _run_hook({"tool_input": {"command": "gh pr create --title test"}})
        result = json.loads(output)
        self.assertIn("systemMessage", result)

    def test_bare_git_commit_triggers_review(self):
        output = _run_hook({"tool_input": {"command": "git commit"}})
        result = json.loads(output)
        self.assertIn("systemMessage", result)

    def test_git_status_does_not_trigger(self):
        output = _run_hook({"tool_input": {"command": "git status"}})
        self.assertEqual(output.strip(), "{}")

    def test_git_diff_does_not_trigger(self):
        output = _run_hook({"tool_input": {"command": "git diff"}})
        self.assertEqual(output.strip(), "{}")

    def test_ls_does_not_trigger(self):
        output = _run_hook({"tool_input": {"command": "ls -la"}})
        self.assertEqual(output.strip(), "{}")

    def test_empty_command_does_not_trigger(self):
        output = _run_hook({"tool_input": {"command": ""}})
        self.assertEqual(output.strip(), "{}")

    def test_missing_command_does_not_trigger(self):
        output = _run_hook({"tool_input": {}})
        self.assertEqual(output.strip(), "{}")

    def test_git_committed_substring_does_not_trigger(self):
        """Ensure 'git commit' only matches at word boundary."""
        output = _run_hook({"tool_input": {"command": "git committed"}})
        self.assertEqual(output.strip(), "{}")

    def test_malformed_json_handled(self):
        """Malformed input should produce empty JSON, not crash."""
        with (
            patch("sys.stdin", StringIO("not json")),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
            patch("sys.exit", side_effect=SystemExit),
        ):
            with contextlib.suppress(SystemExit):
                main()
            self.assertEqual(mock_stdout.getvalue().strip(), "{}")


if __name__ == "__main__":
    unittest.main()
