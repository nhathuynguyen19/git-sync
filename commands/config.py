import os
import click

def show_config(app):
    click.echo("Current Configuration:")
    click.echo(f"  Base Directory: {app.base_dir}")
    click.echo(f"  Remote: {app.remote}")
    click.echo(f'  Commit Message: "{app.commit_message}"')
    click.echo(f"  Auto Mode: {app.auto_mode}")
    click.echo(f"  Auto List File: {app.auto_list_file if app.auto_list_file else 'None'}")

def set_config(app, args):
    if len(args) < 2:
        click.echo("Usage: set <option> <value>")
        click.echo("Options: base_dir, remote, commit_message, auto_mode, auto_list")
        return

    option = args[0].lower()
    value = args[1]

    if option == "base_dir":
        new_path = os.path.expanduser(value)
        if os.path.isdir(new_path):
            app.base_dir = new_path
            click.echo(f"Base directory set to: {app.base_dir}")
        else:
            click.echo(f"Error: Directory '{value}' not found.")
    elif option == "remote":
        app.remote = value
        click.echo(f"Remote set to: {app.remote}")
    elif option == "commit_message":
        app.commit_message = value
        click.echo(f"Commit message set to: '{app.commit_message}'")
    elif option == "auto_mode":
        if value.lower() in ("true", "1", "on"):
            app.auto_mode = True
            click.echo("Auto mode enabled.")
        elif value.lower() in ("false", "0", "off"):
            app.auto_mode = False
            click.echo("Auto mode disabled.")
        else:
            click.echo("Invalid value for auto_mode. Use true/false, 1/0, or on/off.")
    elif option == "auto_list":
        new_path = os.path.expanduser(value)
        if os.path.exists(new_path):
            app.auto_list_file = new_path
            click.echo(f"Auto list file set to: {app.auto_list_file}")
        else:
            click.echo(f"Error: Auto list file '{value}' not found.")
    else:
        click.echo(f"Unknown option: {option}")
