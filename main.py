import os
from shlex import split

import click

from commands import (
    list_repos,
    pull_repos,
    push_repos,
    status_repos,
    check_non_repos,
    show_config,
    set_config,
)


class GitSyncApp:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/mygit")
        self.remote = "origin"
        self.commit_message = "sync: auto commit before sync"
        self.auto_mode = False
        self.auto_list_file = None
        self.prompt = "git-sync> "

    def run(self):
        click.echo("Welcome to git-sync interactive shell!")
        click.echo("Type 'help' for a list of commands.")

        while True:
            try:
                command_line = click.prompt(
                    self.prompt, prompt_suffix="", show_default=False
                ).strip()
                if not command_line:
                    continue

                args = split(command_line)
                command = args[0].lower()
                cmd_args = args[1:]

                if command in ("exit", "quit", "q"):
                    click.echo("Exiting git-sync. Goodbye!")
                    break
                elif command == "list":
                    list_repos(self)
                elif command == "pull":
                    pull_repos(self)
                elif command == "push":
                    push_repos(self)
                elif command == "status":
                    status_repos(self)
                elif command == "check-non-repos":
                    check_non_repos(self)
                elif command == "config":
                    show_config(self)
                elif command == "set":
                    set_config(self, cmd_args)
                elif command == "help":
                    self._show_help()
                else:
                    click.echo(
                        f"Unknown command: '{command}'. Type 'help' for available commands."
                    )
            except EOFError:  # Ctrl+D
                click.echo("\nExiting git-sync. Goodbye!")
                break
            except Exception as e:
                click.echo(f"An unexpected error occurred: {e}")

    def _show_help(self):
        click.echo("Available commands:")
        click.echo("  list        - List all detected git repositories.")
        click.echo("  pull        - Run git pull on all repositories.")
        click.echo(
            "  push        - Stage all changes, commit, and push for all repositories."
        )
        click.echo("  status      - Show git status for all repositories.")
        click.echo(
            "  check-non-repos - List directories in base_dir that are not git repositories."
        )
        click.echo("  config      - Show current configuration settings.")
        click.echo(
            "  set <option> <value> - Set a configuration option (base_dir, remote, commit_message, auto_mode, auto_list)."
        )
        click.echo("  help        - Show this help message.")
        click.echo("  exit / quit / q - Exit the git-sync shell.")


if __name__ == "__main__":
    app = GitSyncApp()
    app.run()
