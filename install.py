#!/usr/bin/env python3
"""Install or package the portable skill and its slash-command templates."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILL_NAME = "spec-driven-development"
SKILL_SOURCE = ROOT / SKILL_NAME
PLUGIN_ROOT = ROOT / "plugins" / "sdd"
COMMANDS_SOURCE = PLUGIN_ROOT / "commands"
IGNORED_FILES = {".DS_Store"}
IGNORED_DIRECTORIES = {"__pycache__"}
MANUAL_ONLY_FIELD = "disable-model-invocation: true"
USER_INVOCABLE_FIELD = "user-invocable: true"


def require_skill() -> None:
    skill_file = SKILL_SOURCE / "SKILL.md"
    if not skill_file.is_file():
        raise SystemExit(f"Missing skill entrypoint: {skill_file}")


def require_commands() -> None:
    commands = sorted(COMMANDS_SOURCE.glob("*.md"))
    if not commands:
        raise SystemExit(f"Missing Codex plugin commands: {COMMANDS_SOURCE}")


def stage_name(source: Path) -> str:
    return f"sdd-{source.stem}"


def portable_command_name(source: Path) -> str:
    return f"{stage_name(source)}.md"


def copy_tree(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{destination.name}-", dir=destination.parent
    ) as temporary:
        staged = Path(temporary) / destination.name
        ignored = shutil.ignore_patterns(*IGNORED_FILES, *IGNORED_DIRECTORIES)
        shutil.copytree(source, staged, ignore=ignored)
        if destination.exists():
            shutil.rmtree(destination)
        staged.replace(destination)


def install(
    destination_root: Path,
    command_destination: Path | None,
    force: bool,
) -> None:
    require_skill()
    destination = destination_root / SKILL_NAME
    if destination.exists() and not force:
        raise SystemExit(
            f"Destination already exists: {destination}\nPass --force to replace it."
        )

    if command_destination is not None:
        require_commands()
        conflicts = [
            command_destination / portable_command_name(source)
            for source in sorted(COMMANDS_SOURCE.glob("*.md"))
            if (command_destination / portable_command_name(source)).exists()
        ]
        if conflicts and not force:
            joined = "\n".join(str(path) for path in conflicts)
            raise SystemExit(
                f"Command files already exist:\n{joined}\n"
                "Pass --force to replace them."
            )

    copy_tree(SKILL_SOURCE, destination)
    print(f"Installed {SKILL_NAME}: {destination}")

    if command_destination is None:
        return

    command_destination.mkdir(parents=True, exist_ok=True)
    for source in sorted(COMMANDS_SOURCE.glob("*.md")):
        shutil.copy2(source, command_destination / portable_command_name(source))
    print(f"Installed slash commands: {command_destination}")


def sync_codex_plugin() -> None:
    require_skill()
    require_commands()
    manifest = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    if not manifest.is_file():
        raise SystemExit(f"Missing Codex plugin manifest: {manifest}")

    copy_tree(SKILL_SOURCE, PLUGIN_ROOT / "skills" / SKILL_NAME)
    print(f"Synchronized Codex plugin skill: {PLUGIN_ROOT / 'skills'}")


def manual_stage_skill_content(source: Path) -> str:
    content = source.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise SystemExit(f"Invalid command frontmatter: {source}")
    frontmatter = f"name: {stage_name(source)}\n{parts[1].strip()}"
    if MANUAL_ONLY_FIELD not in frontmatter:
        frontmatter = f"{frontmatter}\n{MANUAL_ONLY_FIELD}"
    if USER_INVOCABLE_FIELD not in frontmatter:
        frontmatter = f"{frontmatter}\n{USER_INVOCABLE_FIELD}"
    return f"---\n{frontmatter}\n---{parts[2]}"


def claude_root(scope: str, project: Path | None) -> Path:
    if scope == "user":
        return Path.home() / ".claude"
    target = (project or Path.cwd()).expanduser().resolve()
    return target / ".claude"


def install_stage_skills(
    base: Path,
    force: bool,
    product: str,
    surface_note: str,
) -> None:
    require_skill()
    require_commands()
    skill_destination = base / "skills" / SKILL_NAME
    stage_destinations = [
        base / "skills" / stage_name(source)
        for source in sorted(COMMANDS_SOURCE.glob("*.md"))
    ]

    conflicts = []
    if skill_destination.exists():
        conflicts.append(skill_destination)
    conflicts.extend(path for path in stage_destinations if path.exists())
    if conflicts and not force:
        joined = "\n".join(str(path) for path in conflicts)
        raise SystemExit(
            f"{product} files already exist:\n{joined}\n"
            "Pass --force to replace them."
        )

    copy_tree(SKILL_SOURCE, skill_destination)
    for source, destination in zip(
        sorted(COMMANDS_SOURCE.glob("*.md")), stage_destinations
    ):
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "SKILL.md").write_text(
            manual_stage_skill_content(source), encoding="utf-8"
        )
    print(f"Installed {product} skill: {skill_destination}")
    print(f"Installed {product} slash skills: {base / 'skills'}")
    print(surface_note)


def install_claude(scope: str, project: Path | None, force: bool) -> None:
    install_stage_skills(
        claude_root(scope, project),
        force,
        "Claude Code",
        "Claude Code CLI and VS Code extension share this local configuration.",
    )


def copilot_root(scope: str, project: Path | None) -> Path:
    if scope == "user":
        return Path.home() / ".copilot"
    target = (project or Path.cwd()).expanduser().resolve()
    return target / ".github"


def install_copilot(scope: str, project: Path | None, force: bool) -> None:
    install_stage_skills(
        copilot_root(scope, project),
        force,
        "GitHub Copilot",
        "GitHub Copilot in VS Code and GitHub Copilot CLI share Agent Skills.",
    )


def package(output: Path, force: bool) -> None:
    require_skill()
    require_commands()
    if output.exists() and not force:
        raise SystemExit(f"Archive already exists: {output}\nPass --force to replace it.")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(SKILL_SOURCE.rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(SKILL_SOURCE)
            if source.name in IGNORED_FILES or any(
                part in IGNORED_DIRECTORIES for part in relative.parts
            ):
                continue
            archive.write(source, Path(SKILL_NAME) / relative)
        for source in sorted(COMMANDS_SOURCE.glob("*.md")):
            archive.write(
                source, Path("commands") / portable_command_name(source)
            )
    print(f"Created portable archive: {output}")


def package_claude(output: Path, force: bool) -> None:
    require_skill()
    require_commands()
    if output.exists() and not force:
        raise SystemExit(f"Archive already exists: {output}\nPass --force to replace it.")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(SKILL_SOURCE.rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(SKILL_SOURCE)
            if source.name in IGNORED_FILES or any(
                part in IGNORED_DIRECTORIES for part in relative.parts
            ):
                continue
            archive.write(
                source,
                Path("claude-code") / ".claude" / "skills" / SKILL_NAME / relative,
            )
        for source in sorted(COMMANDS_SOURCE.glob("*.md")):
            archive.writestr(
                str(
                    Path("claude-code")
                    / ".claude"
                    / "skills"
                    / stage_name(source)
                    / "SKILL.md"
                ),
                manual_stage_skill_content(source),
            )
    print(f"Created Claude Code archive: {output}")


def package_copilot(output: Path, force: bool) -> None:
    require_skill()
    require_commands()
    if output.exists() and not force:
        raise SystemExit(f"Archive already exists: {output}\nPass --force to replace it.")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(SKILL_SOURCE.rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(SKILL_SOURCE)
            if source.name in IGNORED_FILES or any(
                part in IGNORED_DIRECTORIES for part in relative.parts
            ):
                continue
            archive.write(
                source,
                Path("copilot")
                / ".github"
                / "skills"
                / SKILL_NAME
                / relative,
            )
        for source in sorted(COMMANDS_SOURCE.glob("*.md")):
            archive.writestr(
                str(
                    Path("copilot")
                    / ".github"
                    / "skills"
                    / stage_name(source)
                    / "SKILL.md"
                ),
                manual_stage_skill_content(source),
            )
    print(f"Created GitHub Copilot archive: {output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser(
        "install",
        help="Copy the skill into a host-provided skills directory.",
    )
    install_parser.add_argument(
        "--dest",
        required=True,
        type=Path,
        help="Directory scanned by the agent for skill folders.",
    )
    install_parser.add_argument(
        "--commands-dest",
        type=Path,
        help="Optional directory scanned by the agent for Markdown slash commands.",
    )
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing installation.",
    )

    package_parser = subparsers.add_parser(
        "package",
        help="Create a portable zip containing the skill folder.",
    )
    package_parser.add_argument("--output", required=True, type=Path)
    package_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing archive.",
    )

    subparsers.add_parser(
        "sync-codex",
        help="Copy the canonical skill into the bundled Codex plugin.",
    )

    claude_parser = subparsers.add_parser(
        "install-claude",
        help="Install the core skill and slash-invocable stage skills for Claude Code CLI and VS Code.",
    )
    claude_parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install for all local Claude Code sessions or only one project.",
    )
    claude_parser.add_argument(
        "--project",
        type=Path,
        help="Project directory for --scope project. Defaults to the current directory.",
    )
    claude_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing Claude Code files.",
    )

    claude_package_parser = subparsers.add_parser(
        "package-claude",
        help="Create a zip containing Claude Code CLI and VS Code slash-skill files.",
    )
    claude_package_parser.add_argument("--output", required=True, type=Path)
    claude_package_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing archive.",
    )

    copilot_parser = subparsers.add_parser(
        "install-copilot",
        help="Install skill-based slash commands for GitHub Copilot in VS Code and Copilot CLI.",
    )
    copilot_parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install for all Copilot sessions or only one project.",
    )
    copilot_parser.add_argument(
        "--project",
        type=Path,
        help="Project directory for --scope project. Defaults to the current directory.",
    )
    copilot_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing GitHub Copilot files.",
    )

    copilot_package_parser = subparsers.add_parser(
        "package-copilot",
        help="Create a zip containing GitHub Copilot VS Code and CLI skill files.",
    )
    copilot_package_parser.add_argument("--output", required=True, type=Path)
    copilot_package_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing archive.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "install":
        command_destination = (
            args.commands_dest.expanduser()
            if args.commands_dest is not None
            else None
        )
        install(args.dest.expanduser(), command_destination, args.force)
    elif args.command == "sync-codex":
        sync_codex_plugin()
    elif args.command == "install-claude":
        install_claude(args.scope, args.project, args.force)
    elif args.command == "install-copilot":
        install_copilot(args.scope, args.project, args.force)
    elif args.command == "package-claude":
        package_claude(args.output.expanduser(), args.force)
    elif args.command == "package-copilot":
        package_copilot(args.output.expanduser(), args.force)
    elif args.command == "package":
        package(args.output.expanduser(), args.force)


if __name__ == "__main__":
    main()
