#!/usr/bin/env python3

import subprocess
import shutil
import os
import sys
from pathlib import Path
import click

def run(cmd, check=True, capture_output=False, cwd=None):
    """Run shell command."""
    print(f"⚙️  {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=True, cwd=cwd)
    if capture_output:
        return result.stdout.strip()
    return None

def branch_exists(branch):
    """Check if a Git branch exists locally."""
    try:
        run(f"git rev-parse --verify {branch}", check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

@click.command()
@click.option('--commit-message', prompt="📜 Enter your commit message", help="The Git commit message.")
@click.option('--git-remote', prompt="🛰️ Enter the Git remote to push to", default="origin", show_default=True, help="Git remote name.")
@click.option('--ghp-remote', prompt="🚀 Enter the remote for ghp-import", default="origin", show_default=True, help="Remote for ghp-import deployment.")
def main(commit_message, git_remote, ghp_remote):
    """Deploy the Jupyter Book with cleaning, building, and ghp-import."""
    
    # Move to 'ensi/' directory
    os.chdir(Path(__file__).resolve().parents[1])

    # Get current branch after cd into project
    current_branch = run("git branch --show-current", capture_output=True) or "main"
    git_branch = click.prompt("🌿 Enter the Git branch to push to", default=current_branch, show_default=True)

    # Validate branch
    if not branch_exists(git_branch):
        click.secho(f"❌ Branch '{git_branch}' does not exist. Please create it first.", fg="red")
        sys.exit(1)

    # Warn if pushing to main
    if git_branch == "main":
        confirm = click.prompt("⚠️  WARNING: You are pushing to 'main'. Type 'confirm' to proceed", default="", show_default=False)
        if confirm != "confirm":
            click.secho("🛑 Cancelled push to main.", fg="red")
            sys.exit(1)

    # 🪛 Clean and build
    click.secho("🧼 Cleaning Jupyter Book...", fg="cyan")
    try:
        run("jb clean .")
    except:
        click.secho("⚠️ jb clean failed (maybe already clean).", fg="yellow")

    if os.path.exists("bash/bash_clean.sh"):
        try:
            run("bash/bash_clean.sh")
        except:
            click.secho("ℹ️ No extended clean script found.", fg="yellow")

    click.secho("🏗️ Building Jupyter Book...", fg="cyan")
    try:
        run("jb build .")
    except:
        click.secho("❌ Jupyter Book build failed.", fg="red")
        sys.exit(1)

    # 🍱 Copy extra folders
    click.secho("📦 Copying extra folders...", fg="cyan")
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

    # ✂️ Check if build changed
    click.secho("🔍 Checking if _build/html has changes...", fg="cyan")
    tmp_dir = "/tmp/temp-ghp-check"
    try:
        run(f"git worktree add {tmp_dir} gh-pages")
    except:
        pass

    if os.path.exists(tmp_dir):
        try:
            diff = subprocess.run(["diff", "-r", "_build/html", tmp_dir], capture_output=True)
            if diff.returncode == 0:
                click.secho("🧘 No changes detected. Skipping ghp-import.", fg="green")
            else:
                click.secho("🚀 Changes detected. Deploying with ghp-import...", fg="cyan")
                run(f"ghp-import -n -p -f -r {ghp_remote} _build/html")
        finally:
            run(f"git worktree remove {tmp_dir} --force")
            shutil.rmtree(tmp_dir, ignore_errors=True)

    # 🦈 Plant flicks
    click.secho("🌿 Planting flicks...", fg="cyan")
    try:
        run("python python/plant_flicks_frac.py --percent 23")
    except:
        click.secho("⚠️ Flick planting encountered issues.", fg="yellow")

    # 🏝️ Commit and push
    click.secho("🧾 Staging changes...", fg="cyan")
    run("git add .")

    click.secho("✍️ Committing...", fg="cyan")
    try:
        run(f"git commit -m \"{commit_message}\"")
        click.secho(f"⬆️ Pushing to [{git_remote}/{git_branch}]...", fg="cyan")
        run(f"git push {git_remote} {git_branch}")
    except:
        click.secho("⚠️ Nothing committed. Skipping push.", fg="yellow")

if __name__ == "__main__":
    main()
