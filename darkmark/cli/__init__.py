# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
import hashlib
from pathlib import Path
import time

from rich.console import Console
import typer

from darkmark.cli.common import verbose_callback
from darkmark.console import console
from darkmark.darkmark import DarkMark

from ..__about__ import __version__, name


def version_callback(value: bool) -> None:
    if value:
        console.print(f"{__version__}")
        raise typer.Exit()


app = typer.Typer(
    name=name,
    help="run code blocks in markdown",
)


def get_hash(file, retries=5, sleep=1):
    try:
        new_hash = hashlib.md5(Path(file).read_text().encode()).hexdigest()
    except FileNotFoundError:
        if retries > 0:
            time.sleep(sleep)
            return get_hash(file, retries - 1, sleep)
        raise typer.Exit(1)

    return new_hash


@app.callback(invoke_without_command=True)
def main(
    file: Path = typer.Argument(...),
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,  # is_eager=True
    ),
    debug: bool = typer.Option(None, "--debug", help="start with debug mode running"),
    dry_run: bool = typer.Option(False, help="run without saving"),
    sexp: bool = typer.Option(False, help="print the sexp of the document"),
    clear: bool = typer.Option(False, help="clear existing darkmarks"),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
    watch: bool = typer.Option(False, help="rerun when file changes"),
) -> None:
    if watch:
        old_hash = ""
        while True:
            if get_hash(file) != old_hash:
                console.log("running")
                console.log(f"old_hash: {old_hash}")
                console.log(f"new_hash: {get_hash(file)}")
                d = DarkMark(file)
                d.clear()
                d.run_cells()
                d.write_text()
                time.sleep(1)
                old_hash = hashlib.md5(Path(file).read_text().encode()).hexdigest()

    d = DarkMark(file)
    d.clear()

    if clear and dry_run:
        Console().print(d.md)
        return
    elif clear:
        d.write_text()
        return

    d.run_cells()

    if sexp:
        Console().print(d.sexp())
        return
    if dry_run:
        Console().print(d.md)
        return
    else:
        d.write_text()
