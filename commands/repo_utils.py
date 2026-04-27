import os
import click

def get_git_repos(app):
    """Finds all directories containing a .git folder."""
    repos = []
    
    if not os.path.exists(app.base_dir):
        click.echo(f"Error: Base directory {app.base_dir} does not exist.")
        return repos

    for item in os.listdir(app.base_dir):
        item_path = os.path.join(app.base_dir, item)
        if os.path.isdir(item_path):
            if os.path.exists(os.path.join(item_path, ".git")):
                repos.append(item_path)
    return repos

def get_repos_to_process(app):
    all_repos_paths = get_git_repos(app)
    if app.auto_mode and app.auto_list_file:
        repos_to_process = []
        try:
            with open(app.auto_list_file, "r") as f:
                auto_repo_names = {line.strip() for line in f if line.strip()}
                
            for repo_path in all_repos_paths:
                if os.path.basename(repo_path) in auto_repo_names:
                    repos_to_process.append(repo_path)
        except FileNotFoundError:
            click.echo(f"Error: Auto list file not found at {app.auto_list_file}")
            return []
        except Exception as e:
            click.echo(f"Error reading auto list file: {e}")
            return []
        return repos_to_process
    else:
        return all_repos_paths
