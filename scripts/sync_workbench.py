#!/usr/bin/env python3
"""Sync claude-workbench rules and plugin settings to a consumer project.

Usage:
    python scripts/sync_workbench.py rust --source /path/to/workbench
    python scripts/sync_workbench.py rust --source . --target /other/project
    python scripts/sync_workbench.py rust --source . --rules-only
    python scripts/sync_workbench.py rust --source . --settings-only
    python scripts/sync_workbench.py rust --source . --check
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

GENERATED_HEADER = "<!-- managed by sync-workbench — do not edit manually -->\n\n"


def load_workbench_config(source: Path) -> dict:
    """Load workbench.json from a local workbench directory."""
    config_path = source / "workbench.json"
    if not config_path.exists():
        logger.error("workbench.json not found at %s", config_path)
        sys.exit(1)
    return json.loads(config_path.read_text(encoding="utf-8"))


def sync_rules(source: Path, profile: dict, target: Path) -> list[str]:
    """Copy rule files from workbench to target .claude/rules/."""
    rules_directory = target / ".claude" / "rules"
    rules_directory.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    for rule_name in profile["rules"]:
        source_file = source / "rules" / f"{rule_name}.md"
        destination_file = rules_directory / f"{rule_name}.md"

        if not source_file.exists():
            logger.warning("Rule source not found: %s", source_file)
            continue

        content = GENERATED_HEADER + source_file.read_text(encoding="utf-8")

        if destination_file.exists():
            existing = destination_file.read_text(encoding="utf-8")
            if existing == content:
                logger.info("%s: up to date", rule_name)
                continue

        destination_file.write_text(content, encoding="utf-8")
        changed.append(rule_name)
        logger.info("%s: synced", rule_name)

    return changed


def sync_settings(config: dict, profile: dict, target: Path) -> bool:
    """Merge plugin settings into target .claude/settings.json.

    Only touches extraKnownMarketplaces and enabledPlugins.
    All other keys are preserved untouched.
    """
    settings_path = target / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    else:
        settings = {}

    original = json.dumps(settings, sort_keys=True)

    # Merge extraKnownMarketplaces
    if "marketplaces" in config:
        marketplaces = settings.setdefault("extraKnownMarketplaces", {})
        for name, value in config["marketplaces"].items():
            marketplaces[name] = value

    # Merge enabledPlugins (additive — never removes existing entries)
    enabled_plugins = settings.setdefault("enabledPlugins", {})
    for plugin_identifier in profile["plugins"]:
        enabled_plugins[plugin_identifier] = True

    if json.dumps(settings, sort_keys=True) == original:
        logger.info("settings.json: up to date")
        return False

    settings_path.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    logger.info("settings.json: updated")
    return True


def check_rules(source: Path, profile: dict, target: Path) -> list[str]:
    """Check which rules are out of date without writing anything."""
    rules_directory = target / ".claude" / "rules"
    outdated: list[str] = []

    for rule_name in profile["rules"]:
        source_file = source / "rules" / f"{rule_name}.md"
        destination_file = rules_directory / f"{rule_name}.md"

        if not source_file.exists():
            continue

        expected = GENERATED_HEADER + source_file.read_text(encoding="utf-8")

        if not destination_file.exists():
            outdated.append(rule_name)
            continue
        if destination_file.read_text(encoding="utf-8") != expected:
            outdated.append(rule_name)

    return outdated


def check_settings(config: dict, profile: dict, target: Path) -> bool:
    """Check whether settings would change without writing anything."""
    settings_path = target / ".claude" / "settings.json"

    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    else:
        settings = {}

    original = json.dumps(settings, sort_keys=True)

    if "marketplaces" in config:
        marketplaces = settings.setdefault("extraKnownMarketplaces", {})
        for name, value in config["marketplaces"].items():
            marketplaces[name] = value

    enabled_plugins = settings.setdefault("enabledPlugins", {})
    for plugin_identifier in profile["plugins"]:
        enabled_plugins[plugin_identifier] = True

    return json.dumps(settings, sort_keys=True) != original


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync claude-workbench rules and settings to a project",
    )
    parser.add_argument(
        "profile",
        help="Profile name (base, rust, python, full)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to local workbench clone",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("."),
        help="Target project directory (default: current directory)",
    )
    parser.add_argument(
        "--rules-only",
        action="store_true",
        help="Only sync rules",
    )
    parser.add_argument(
        "--settings-only",
        action="store_true",
        help="Only sync settings",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if anything is out of date without writing files",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        stream=sys.stderr,
    )

    config = load_workbench_config(args.source)
    target = args.target.resolve()

    profile_name = args.profile
    if profile_name not in config["profiles"]:
        available = ", ".join(config["profiles"])
        logger.error(
            "Unknown profile: %s (available: %s)",
            profile_name,
            available,
        )
        sys.exit(1)

    profile = config["profiles"][profile_name]

    # Check mode — read-only
    if args.check:
        rules_outdated = check_rules(args.source, profile, target)
        settings_outdated = check_settings(config, profile, target)

        if not rules_outdated and not settings_outdated:
            print("Everything is in sync.")
        else:
            if rules_outdated:
                print(f"Rules out of date: {', '.join(rules_outdated)}")
            if settings_outdated:
                print("Settings out of date")
            sys.exit(1)
        return

    # Sync mode
    sync_both = not args.rules_only and not args.settings_only
    rules_changed: list[str] = []
    settings_changed = False

    if sync_both or args.rules_only:
        rules_changed = sync_rules(args.source, profile, target)

    if sync_both or args.settings_only:
        settings_changed = sync_settings(config, profile, target)

    if not rules_changed and not settings_changed:
        print("Everything is up to date.")
    else:
        if rules_changed:
            print(f"Rules synced: {', '.join(rules_changed)}")
        if settings_changed:
            print("Settings updated.")


if __name__ == "__main__":
    main()
