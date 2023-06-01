# DarkMark

<img src="https://user-images.githubusercontent.com/22648375/216847624-d4dbc93b-76d7-4d2c-ba71-fa58b4b331e5.png" alt="darkmark" width="250" align=right>


Runs codeblocks marked with the darkmark, and inserts the results.  

DarkMark uses tree-sitter to identify codeblocks.  Currently it only supports python codeblocks in markdown files and runs them with ipython.  Handy for writing docs/blog posts so you can stay right in your markdown editor of choice and get the outputs in line.  No need to jump into a whole other tool just to do live execution.

---

## Installation

```console
pip install darkmark
```

```console
❯ darkmark --help

 Usage: darkmark [OPTIONS] COMMAND [ARGS]...

 run code blocks in markdown

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell.       │
│                                                              [default: None]                                   │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy  │
│                                                              it or customize the installation.                 │
│                                                              [default: None]                                   │
│ --help                                                       Show this message and exit.                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ run                                                                                                            │
│ sexp                                                                                                           │
│ tui                                                                                                            │
│ watch                                                                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Usage

Mark your codeblocks with the darkmark.

~~~ markdown
```python {.python .darkmark}
r = requests.get('https://waylonwalker.com')
r.status_code
```
~~~

Then run `darkmark <file>.md` and darkmark will insert the results of the codeblock.

~~~ markdown
``` {.console .darkmark_output}
200
```
~~~

## Automatic imports

Automatic imports are provided by [pyflyby](https://github.com/deshaw/pyflyby).

## Supported Languages

Currently the only language supported is python.

* python

## Example

Running `darkmark watch <file.md>` updates the file on save.

[darkmark.webm](https://user-images.githubusercontent.com/22648375/216849738-12897dfc-3e2b-4e5b-9b6d-cbb29c3ae782.webm)

## License

`darkmark` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
