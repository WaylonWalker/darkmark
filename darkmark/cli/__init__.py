# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
import hashlib
from pathlib import Path
import time

from rich.console import Console
from rich.markdown import Markdown
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


@app.command()
def tui(ctx: typer.Context) -> None:
    try:
        from trogon import Trogon
        from typer.main import get_group
    except ImportError:
        typer.echo("trogon not installed")
        typer.echo(
            "install markata with optional tui group to use tui `pip install 'darkmark[tui]'`"
        )
        return

    Trogon(get_group(app), click_context=ctx).run()


def get_hash(file, retries=5, sleep=1):
    try:
        new_hash = hashlib.md5(Path(file).read_text().encode()).hexdigest()
    except FileNotFoundError:
        if retries > 0:
            time.sleep(sleep)
            return get_hash(file, retries - 1, sleep)
        raise typer.Exit(1)

    return new_hash


def _run(file: Path, dry_run: bool, clear: bool, verbose: bool) -> None:
    d = DarkMark(file)
    d.clear()

    if clear and dry_run:
        Console().print(d.md)
        return
    elif clear:
        d.write_text()
        return

    d.run_cells()

    if dry_run:
        md = Markdown(d.md)
        Console().print(md)
        return
    else:
        d.write_text()


@app.command()
def run(
    file: Path = typer.Argument(...),
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,  # is_eager=True
    ),
    debug: bool = typer.Option(None, "--debug", help="start with debug mode running"),
    dry_run: bool = typer.Option(False, help="run without saving"),
    clear: bool = typer.Option(False, help="clear existing darkmarks"),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:
    _run(file=file, dry_run=dry_run, clear=clear, verbose=verbose)


@app.command()
def watch(
    file: Path = typer.Argument(...),
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,  # is_eager=True
    ),
    debug: bool = typer.Option(None, "--debug", help="start with debug mode running"),
    dry_run: bool = typer.Option(False, help="run without saving"),
    clear: bool = typer.Option(False, help="clear existing darkmarks"),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:
    old_hash = ""
    while True:
        if get_hash(file) != old_hash:
            _run(file=file, dry_run=dry_run, clear=clear, verbose=verbose)
            time.sleep(1)
            old_hash = hashlib.md5(Path(file).read_text().encode()).hexdigest()


@app.command()
def sexp(
    file: Path = typer.Argument(...),
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,  # is_eager=True
    ),
    debug: bool = typer.Option(None, "--debug", help="start with debug mode running"),
    clear: bool = typer.Option(False, help="clear existing darkmarks"),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:

    d = DarkMark(file)
    Console().print(d.sexp())
    return
