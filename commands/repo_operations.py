import os
import time
import click
from git import Repo, exc
from .repo_utils import get_git_repos, get_repos_to_process

def list_repos(app):
    """List all detected git repositories."""
    repos = get_git_repos(app)
    if not repos:
        click.echo("No git repositories found.")
        return

    click.echo(f"Found {len(repos)} repositories in {app.base_dir}:")
    for repo in repos:
        click.echo(f" - {os.path.basename(repo)}")

def pull_repos(app):
    """Run git pull on all repositories."""
    repos = get_repos_to_process(app)
    for repo_path in repos:
        repo_name = os.path.basename(repo_path)
        try:
            repo = Repo(repo_path)
            if repo.is_dirty():
                click.echo(f"[{repo_name}] Skipping pull: Repository has uncommitted changes.")
                continue

            click.echo(f"[{repo_name}] Pulling latest changes...")
            origin = repo.remotes[app.remote]
            origin.pull()
            click.echo(f"[{repo_name}] Successfully updated.")
        except exc.GitCommandError as e:
            click.echo(f"[{repo_name}] Error during pull: {e}")
        except Exception as e:
            click.echo(f"[{repo_name}] Unexpected error during pull: {e}")
        if app.auto_mode:
            time.sleep(0.1)  # Small delay to limit CPU usage

def push_repos(app):
    """Stage all changes, commit, and push for all repositories."""
    repos = get_repos_to_process(app)
    for repo_path in repos:
        repo_name = os.path.basename(repo_path)
        try:
            repo = Repo(repo_path)

            if repo.is_dirty(untracked_files=True):
                click.echo(f"[{repo_name}] Changes detected. Checking status...")
                status_output = repo.git.status(short=True)
                click.echo(f"[{repo_name}] Status:\n{status_output}")

                if app.auto_mode:
                    click.echo(f"[{repo_name}] Auto-mode enabled. Proceeding with push.")
                else:
                    if not click.confirm(f"[{repo_name}] Do you want to stage, commit, and push these changes?"):
                        click.echo(f"[{repo_name}] Skipped push due to user rejection.")
                        continue

                click.echo(f"[{repo_name}] Staging changes...")
                repo.git.add(A=True)
                click.echo(f"[{repo_name}] Committing with message: '{app.commit_message}'...")
                repo.index.commit(app.commit_message)

                click.echo(f"[{repo_name}] Pushing to {app.remote}...")
                origin = repo.remotes[app.remote]
                origin.push()
                click.echo(f"[{repo_name}] Successfully pushed.")
            else:
                click.echo(f"[{repo_name}] No changes to commit.")
        except exc.GitCommandError as e:
            click.echo(f"[{repo_name}] Error during push: {e}")
        except Exception as e:
            click.echo(f"[{repo_name}] Unexpected error during push: {e}")
        if app.auto_mode:
            time.sleep(0.1)  # Small delay to limit CPU usage

def status_repos(app):
    """Show git status for all repositories."""
    repos = get_git_repos(app)
    for repo_path in repos:
        repo_name = os.path.basename(repo_path)
        try:
            repo = Repo(repo_path)
            status_text = "Clean" if not repo.is_dirty() else "Dirty (Uncommitted changes)"
            click.echo(f"[{repo_name}] {status_text}")
        except exc.InvalidGitRepositoryError:
            click.echo(f"[{repo_name}] Not a valid git repository.")
        except Exception as e:
            click.echo(f"[{repo_name}] Error getting status: {e}")

def check_non_repos(app):
    """Checks for and lists directories in base_dir that are not git repositories."""
    click.echo(f"Checking for non-Git repositories in {app.base_dir}...")
    non_repos = []
    base_path = os.path.expanduser(app.base_dir)

    if not os.path.exists(base_path):
        click.echo(f"Error: Base directory {base_path} does not exist.")
        return

    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            if not os.path.exists(os.path.join(item_path, ".git")):
                non_repos.append(item_path)

    if not non_repos:
        click.echo("No non-Git repository directories found.")
    else:
        click.echo("Found the following non-Git repository directories:")
        for non_repo_path in non_repos:
            click.echo(f" - {os.path.basename(non_repo_path)}")
