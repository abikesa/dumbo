#!/usr/bin/env python3

import subprocess
import shutil
import os
import sys
from pathlib import Path
import click

def run(cmd, check=True, capture_output=False, cwd=None):
    """Run a shell command with optional output capture."""
    print(f"⚙️  {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=True, cwd=cwd)
    if capture_output:
        return result.stdout.strip()
    return None

def branch_exists(branch):
    """Check if a Git branch exists locally."""
    try:
        run(f"git rev-parse --verify {branch}  # checks if the branch exists locally", capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

@click.command()
@click.option('--commit-message', prompt="📜 Enter your commit message", help="The Git commit message.")
@click.option('--git-remote', prompt="🛰️ Enter the Git remote to push to", default="origin", show_default=True, help="Git remote name.")
@click.option('--ghp-remote', prompt="🚀 Enter the remote for ghp-import", default="origin", show_default=True, help="Remote for ghp-import deployment.")
def main(commit_message, git_remote, ghp_remote):
    """Automate the full deploy cycle for a Jupyter Book project."""

    os.chdir(Path(__file__).resolve().parents[1])  # move into 'ensi/' parent directory

    # Get current Git branch
    current_branch = run("git branch --show-current  # shows the current branch", capture_output=True) or "main"
    git_branch = click.prompt("🌿 Enter the Git branch to push to", default=current_branch, show_default=True)

    if not branch_exists(git_branch):
        click.secho(f"❌ Branch '{git_branch}' does not exist.", fg="red")
        sys.exit(1)

    if git_branch == "main":
        confirm = click.prompt("⚠️  WARNING: Pushing to 'main'. Type 'confirm' to continue", default="", show_default=False)
        if confirm != "confirm":
            click.secho("🛑 Cancelled push to 'main'", fg="red")
            sys.exit(1)

    # Sync with remote
    click.secho("🔄 Fetching remote changes...", fg="cyan")
    run(f"git fetch {git_remote}  # fetches latest from remote")

    click.secho("🔀 Rebasing local changes...", fg="cyan")
    try:
        run(f"git rebase {git_remote}/{git_branch}  # applies local commits on top of remote")
    except:
        click.secho("⚠️ Rebase failed. You may need to resolve conflicts manually.", fg="red")
        sys.exit(1)

    # Clean build environment
    click.secho("🧼 Cleaning Jupyter Book...", fg="cyan")
    run("jb clean .")

    if os.path.exists("bash/bash_clean.sh"):
        run("bash/bash_clean.sh")

    # Build the book
    click.secho("🏗️ Building Jupyter Book...", fg="cyan")
    run("jb build .")

    # Copy extra directories into _build/html
    click.secho("📦 Copying extra folders...", fg="cyan")
    extras = [
        "pdfs", "figures", "media", "testbin", "nis", "myhtml", "dedication", "python", "ai",
        "r", "stata", "bash", "xml", "data", "aperitivo", "antipasto", "primo", "secondo",
        "contorno", "insalata", "formaggio-e-frutta", "dolce", "caffe", "digestivo", "ukubona"
    ]
    for d in extras:
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

    # Deploy with ghp-import if changes exist
    click.secho("🔍 Checking if _build/html has changed...", fg="cyan")
    tmp_dir = "/tmp/temp-ghp-check"
    run(f"git worktree add {tmp_dir} gh-pages  # temp checkout of gh-pages")

    try:
        diff = subprocess.run(["diff", "-r", "_build/html", tmp_dir], capture_output=True)
        if diff.returncode == 0:
            click.secho("🧘 No changes detected in HTML.", fg="green")
        else:
            click.secho("🚀 Deploying with ghp-import...", fg="cyan")
            run(f"ghp-import -n -p -f -r {ghp_remote} _build/html")
    finally:
        run(f"git worktree remove {tmp_dir} --force  # clean up temp worktree")
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Flicks
    click.secho("🌿 Planting flicks...", fg="cyan")
    try:
        run("python python/plant_flicks_frac.py --percent 23")
    except:
        click.secho("⚠️ Flick planting failed", fg="yellow")

    # Git add/commit/push
    click.secho("🧾 Staging changes...", fg="cyan")
    run("git add .  # stages all changes")

    click.secho("✍️ Committing...", fg="cyan")
    try:
        run(f"git commit -m \"{commit_message}\"  # commit with message")
        click.secho(f"⬆️ Pushing to {git_remote}/{git_branch}...", fg="cyan")
        if git_branch == "main":
            run(f"git pull --rebase {git_remote} main && git push {git_remote} main")
        else:
            run(f"git push {git_remote} {git_branch}  # push to remote")
    except:
        click.secho("⚠️ Nothing to commit or push.", fg="yellow")

if __name__ == "__main__":
    main()
