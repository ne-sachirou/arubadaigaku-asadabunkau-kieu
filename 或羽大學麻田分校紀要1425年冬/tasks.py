#!/usr/bin/env python3
"""Tasks."""
import os
import subprocess
import sys

tasks = {}


def run(command: str, capture_output=False, text=None) -> subprocess.CompletedProcess:
    """Run command."""
    command = command.strip()
    print("+ ", command)
    env = os.environ.copy()
    return subprocess.run(
        command,
        capture_output=capture_output,
        check=True,
        env=env,
        shell=True,
        text=text,
    )


def task(function):
    """Define a task."""
    if function.__doc__:
        tasks[function.__name__] = function.__doc__

    def wrapper():
        function()

    return wrapper


@task
def format():
    """Format all files."""
    run("poetry run black *.py")
    run("npx prettier --write *.md")


@task
def test():
    """Test."""
    run("poetry check")
    run("npm audit")


@task
def upgrade():
    """Upgrade dependencies."""
    run("npx npm-check-updates -u")
    run("npm install")
    run("npm audit fix")
    run("npm fund")
    run("poetry update")


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        for task_name, describe in tasks.items():
            print(f"{task_name.ljust(16)}\t{describe}")
        exit(0)
    for task_name in sys.argv[1:]:
        locals()[task_name]()
