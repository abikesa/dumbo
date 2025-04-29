#!/usr/bin/env python3

import subprocess
import os
import sys
import shutil

def run(cmd, check=True, capture_output=False, cwd=None):
    """Run shell command."""
    print(f"⚙️  {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=True, cwd=cwd)
    if capture_output:
        return result.stdout.strip()
    return None

def prompt(msg, default=None):
    """Prompt for input with default."""
    if default:
        return input(f"{msg} (default: {default}): ") or default
    return input(f"{msg}: ")

def branch_exists(branch):
    """Check if a Git branch exists locally."""
    try:
        run(f"git rev-parse --verify {branch}", check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    os.chdir(Path(__file__).resolve().parents[1])  # Move to 'ensi/' directory
    
    # 🌊 0. Prompt the navigator
    commit_message = prompt("📜 Enter your commit message")
    
    current_branch = run("git branch --show-current", capture_output=True)
    git_remote = prompt("🛰️ Enter the Git remote to push to", "origin")
    git_branch = prompt("🌿 Enter the Git branch to push to", current_branch)
    ghp_remote = prompt("🚀 Enter the remote for ghp-import", "origin")

    # Check branch exists
    if not branch_exists(git_branch):
        print(f"❌ Branch '{git_branch}' does not exist. Please create it first.")
        sys.exit(1)

    # Warn if trying to push to main
    if git_branch == "main":
        confirm = prompt("⚠️  WARNING: You are about to push to 'main'. Type 'confirm' to proceed")
        if confirm != "confirm":
            print("🛑 Cancelled push to main.")
            sys.exit(1)

    # 🪛 1. Clean and rebuild
    print("🧼 Cleaning Jupyter Book...")
    try:
        run("jb clean .")
    except:
        print("⚠️ jb clean failed (might be clean already).")
    
    if os.path.exists("bash/bash_clean.sh"):
        try:
            run("bash/bash_clean.sh")
        except:
            print("ℹ️ No extended clean script found.")

    print("🏗️ Building Jupyter Book...")
    try:
        run("jb build .")
    except:
        print("❌ Jupyter Book build failed. Exiting.")
        sys.exit(1)

    # 🍱 Inject extra directories
    print("📦 Copying extra folders...")
    extra_dirs = [
        "pdfs", "figures", "media", "testbin", "nis", "myhtml", "dedication", "python", "ai",
        "r", "stata", "bash", "xml", "data", "aperitivo", "antipasto", "primo", "secondo",
        "contorno", "insalata", "formaggio-e-frutta", "dolce", "caffe", "digestivo", "ukubona"
    ]

    for d in extra_dirs:
        if os.path.isdir(d):
            dest = os.path.join("_build/html", d)
            os.makedirs(dest, exist_ok=True)
            for item in os.listdir(d):
                s = os.path.join(d, item)
                d_ = os.path.join(dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d_, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d_)

    # ✂️ 2. Check if _build/html actually changed
    print("🔍 Checking if _build/html has changes...")
    tmp_dir = "/tmp/temp-ghp-check"
    try:
        run(f"git worktree add {tmp_dir} gh-pages")
    except:
        pass  # might already exist

    if os.path.exists(tmp_dir):
        try:
            diff = subprocess.run(["diff", "-r", "_build/html", tmp_dir], capture_output=True)
            if diff.returncode == 0:
                print("🧘 No changes in built HTML. Skipping ghp-import.")
            else:
                print("🚀 Changes detected in build. Deploying with ghp-import...")
                run(f"ghp-import -n -p -f -r {ghp_remote} _build/html")
        finally:
            run(f"git worktree remove {tmp_dir} --force")
            shutil.rmtree(tmp_dir, ignore_errors=True)

    # 🦈 3. Plant flicks
    print("🌿 Planting flicks...")
    try:
        run("python python/plant_flicks_frac.py --percent 23")
    except:
        print("⚠️ Flick planting encountered issues.")

    # 🏝️ 4. Commit and push
    print("🧾 Staging changes...")
    run("git add .")

    print("✍️ Committing...")
    try:
        run(f"git commit -m \"{commit_message}\"")
        print(f"⬆️ Pushing to [{git_remote}/{git_branch}]...")
        run(f"git push {git_remote} {git_branch}")
    except:
        print("⚠️ Nothing committed. Skipping push.")

if __name__ == "__main__":
    from pathlib import Path
    main()
