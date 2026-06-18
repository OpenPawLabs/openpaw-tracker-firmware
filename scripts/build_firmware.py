#!/usr/bin/env python3
"""Build OpenPaw Tracker firmware from a tagged SlimeVR-Tracker-ESP release."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLIMEVR_REPO = "https://github.com/SlimeVR/SlimeVR-Tracker-ESP.git"
DEFAULT_CONFIG_PATH = REPO_ROOT / "board-config.json"
FIRMWARE_CACHE_DIR = REPO_ROOT / ".cache" / "firmware"
DIST_DIR = REPO_ROOT / "dist"

BRANDING_KEYS = (
    "VENDOR_NAME",
    "VENDOR_URL",
    "PRODUCT_NAME",
    "UPDATE_ADDRESS",
    "UPDATE_NAME",
)


class BuildError(RuntimeError):
    pass


def branding_build_flags(branding: dict[str, str]) -> str:
    return " ".join(
        f"-D {key}='\"{branding[key]}\"'" for key in BRANDING_KEYS
    )


def firmware_filename(branding: dict[str, str]) -> str:
    return f"{branding['UPDATE_NAME']}.bin"


def _require_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise BuildError(f"Could not find '{name}' on PATH.")
    return path


def _run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("$ " + " ".join(cmd))
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True)
    if proc.returncode != 0:
        raise BuildError(f"Command failed (exit {proc.returncode}): {' '.join(cmd)}")


def _load_board_config(path: Path) -> tuple[str, dict, dict[str, str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BuildError(f"Board config not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BuildError(f"Invalid JSON in {path}: {exc}") from exc

    board_type = raw.get("type")
    values = raw.get("values")
    branding = raw.get("branding")
    if not isinstance(board_type, str) or not board_type:
        raise BuildError(f"{path}: missing or invalid 'type'")
    if not isinstance(values, dict):
        raise BuildError(f"{path}: missing or invalid 'values'")
    if not isinstance(branding, dict):
        raise BuildError(f"{path}: missing or invalid 'branding'")
    missing = [key for key in BRANDING_KEYS if not branding.get(key)]
    if missing:
        raise BuildError(f"{path}: branding missing required keys: {', '.join(missing)}")
    return board_type, values, {key: str(branding[key]) for key in BRANDING_KEYS}


def _clone_firmware(repo_url: str, tag: str) -> Path:
    if FIRMWARE_CACHE_DIR.exists():
        shutil.rmtree(FIRMWARE_CACHE_DIR)
    FIRMWARE_CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
    _run(
        [
            _require_tool("git"),
            "clone",
            "--depth",
            "1",
            "--branch",
            tag,
            "--single-branch",
            repo_url,
            str(FIRMWARE_CACHE_DIR),
        ]
    )
    if not (FIRMWARE_CACHE_DIR / "platformio.ini").is_file():
        raise BuildError(
            f"Cloned firmware at tag {tag!r} is missing platformio.ini: {FIRMWARE_CACHE_DIR}"
        )
    return FIRMWARE_CACHE_DIR


def build_firmware(
    tag: str,
    *,
    slimevr_repo: str = DEFAULT_SLIMEVR_REPO,
    config_path: Path = DEFAULT_CONFIG_PATH,
    output_dir: Path = DIST_DIR,
) -> Path:
    board_type, values, branding = _load_board_config(config_path)
    firmware_root = _clone_firmware(slimevr_repo, tag)

    env = dict(os.environ)
    env["SLIMEVR_OVERRIDE_DEFAULTS"] = json.dumps(values, separators=(",", ":"))
    env["PLATFORMIO_BUILD_FLAGS"] = branding_build_flags(branding)

    _run([_require_tool("pio"), "run", "-e", board_type], cwd=firmware_root, env=env)

    firmware_bin = firmware_root / ".pio" / "build" / board_type / "firmware.bin"
    if not firmware_bin.is_file():
        raise BuildError(f"Expected firmware not found: {firmware_bin}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / firmware_filename(branding)
    shutil.copy2(firmware_bin, output_path)
    print(f"Built {output_path}")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build OpenPaw Tracker firmware for a SlimeVR-Tracker-ESP release tag."
    )
    parser.add_argument(
        "tag",
        help="SlimeVR-Tracker-ESP release tag to build (for example v0.7.2).",
    )
    parser.add_argument(
        "--slimevr-repo",
        default=DEFAULT_SLIMEVR_REPO,
        help=f"SlimeVR firmware repository URL (default: {DEFAULT_SLIMEVR_REPO}).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to board-config.json.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DIST_DIR,
        help=f"Directory for the built firmware (default: {DIST_DIR}).",
    )
    args = parser.parse_args(argv)

    try:
        build_firmware(
            args.tag,
            slimevr_repo=args.slimevr_repo,
            config_path=args.config,
            output_dir=args.output_dir,
        )
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
