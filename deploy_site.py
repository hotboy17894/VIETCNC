#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy website VietNT lên GitHub Pages.

Cách dùng:
  python deploy_site.py

Yêu cầu:
  - Đã cài Git.
  - Máy đã đăng nhập GitHub sẵn bằng Git Credential Manager, GitHub Desktop hoặc gh auth.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO_URL = "https://github.com/hotboy17894/VIETCNC.git"
BRANCH = "main"
ROOT = Path(__file__).resolve().parent


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=False,
        check=check,
    )


def ensure_git_repo() -> None:
    if shutil.which("git") is None:
        raise RuntimeError("Chưa tìm thấy Git. Hãy cài Git for Windows rồi chạy lại.")

    if not (ROOT / ".git").exists():
        run(["git", "init"])
        run(["git", "remote", "add", "origin", REPO_URL])
    else:
        remotes = subprocess.run(
            ["git", "remote"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=True,
        ).stdout.split()
        if "origin" not in remotes:
            run(["git", "remote", "add", "origin", REPO_URL])


def sync_webvietcnc_copy() -> None:
    web_dir = ROOT / "webvietcnc"
    web_dir.mkdir(exist_ok=True)

    files = [
        "index.html",
        "style.css",
        "script.js",
        "robots.txt",
        "sitemap.xml",
        "update.json",
        "vietnt-preview.png",
    ]
    for name in files:
        source = ROOT / name
        if source.exists():
            shutil.copy2(source, web_dir / name)


def has_changes() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=True,
    )
    return bool(result.stdout.strip())


def current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def deploy(force: bool = False) -> None:
    ensure_git_repo()
    sync_webvietcnc_copy()

    branch = current_branch()
    if branch and branch != BRANCH:
        print(f"Đang ở branch {branch}. Script sẽ push HEAD lên origin/{BRANCH}.")

    run(["git", "add", "-A"])

    if has_changes():
        message = f"Update VietNT website {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run(["git", "commit", "-m", message])
    else:
        print("Không có thay đổi mới để commit.")

    push_cmd = ["git", "push", "origin", f"HEAD:{BRANCH}"]
    if force:
        push_cmd.insert(2, "--force-with-lease")
    run(push_cmd)

    print()
    print("Deploy xong.")
    print("Website: https://vietcnc.site/")
    print("GitHub:  https://github.com/hotboy17894/VIETCNC")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy website VietNT lên GitHub.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Dùng git push --force-with-lease nếu remote từ chối push thường.",
    )
    args = parser.parse_args()

    try:
        deploy(force=args.force)
        return 0
    except subprocess.CalledProcessError as exc:
        print()
        print("Git báo lỗi.")
        print(f"Lệnh lỗi: {' '.join(exc.cmd)}")
        print("Nếu lỗi đăng nhập, hãy đăng nhập GitHub trong Git Credential Manager hoặc GitHub Desktop rồi chạy lại.")
        return exc.returncode or 1
    except Exception as exc:
        print()
        print(f"Lỗi: {exc}")
        return 1
    finally:
        skip_pause = os.environ.get("VIETNT_DEPLOY_SKIP_PY_PAUSE") == "1"
        if not skip_pause and sys.platform.startswith("win") and sys.stdin and sys.stdin.isatty():
            input("\nNhấn Enter để đóng cửa sổ...")


if __name__ == "__main__":
    raise SystemExit(main())
