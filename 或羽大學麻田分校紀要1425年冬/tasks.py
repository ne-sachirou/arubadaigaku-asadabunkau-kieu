#!/usr/bin/env python3
"""Tasks."""
from shlex import quote
import glob
import os
import re
import subprocess
import sys
import typing as t

tasks = {}


class SegziForcer(object):
    """Force 俗字 to 正字."""

    itaizi_selectors: t.List[str] = [
        chr(0xE0100),
        chr(0xE0101),
    ]

    table: t.Dict[str, str] = {
        "\u4e3b": "\u4e3b" + chr(0xE0101),
        "\u4ea4": "\u4ea4" + chr(0xE0101),
        "\u516c": "\u516c" + chr(0xE0101),
        "\u5272": chr(0x2F822),
        "\u535a": "\u535a" + chr(0xE0101),
        "\u5438": "\u5438" + chr(0xE0101),
        "\u5e1d": "\u5e1d" + chr(0xE0101),
        "\u6210": chr(0x2F8B2),
        "\u6240": "\u6240" + chr(0xE0101),
        "\u6587": "\u6587" + chr(0xE0101),
        "\u660e": "\u660e" + chr(0xE0101),
        "\u6700": "\u6700" + chr(0xE0101),
        "\u6b21": "\u6b21" + chr(0xE0101),
        "\u6ca2": "\u6fa4",
        "\u7814": "\u784f",
        "\u795e": "\u795e" + chr(0xE0100),
        "\u8005": "\u8005" + chr(0xE0101),
        "\u8981": "\u8981" + chr(0xE0101),
        "\u8ff0": "\u8ff0" + chr(0xE0101),
        "\u9592": "\u9592" + chr(0xE0101),
        "\u9593": "\u9592" + chr(0xE0101),
        "\u985e": "\u985e" + chr(0xE0100),
        "\uf9d0": "\u985e" + chr(0xE0100),
        "\ufa19": "\u795e" + chr(0xE0100),
        "\ufa5b": "\u8005" + chr(0xE0101),
    }

    def force(self, filename: str) -> bool:
        """Force 俗字 to 正字. Return True if the file had some 俗字."""
        with open(filename, "r+") as f:
            original_content = content = f.read()
            for (zokuzi, segzi) in SegziForcer.table.items():
                regex = "{}(?:[{}]?)".format(
                    zokuzi, "".join(SegziForcer.itaizi_selectors),
                )
                content = re.sub(regex, segzi, content)
            f.seek(0)
            f.truncate()
            f.write(content)
        return original_content != content


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
    for filename in glob.glob("*.md"):
        # run(r"perl -i -pe 'use utf8; s/[\\x{E0100}\\x{E0101}]//g' " + quote(filename))
        # run("npx prettier --write {}".format(quote(filename)))
        if SegziForcer().force(filename):
            print(filename, " !")
        else:
            print(filename)


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
