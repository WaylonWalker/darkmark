import io
import os
from pathlib import Path
import sys

from IPython.terminal.interactiveshell import TerminalInteractiveShell
from tree_sitter_languages import get_language, get_parser

from darkmark import replacer
from darkmark.console import console

os.environ["NO_COLOR"] = "1"

DARKMARK_INFO = "darkmark_output"


class DarkMark:
    def __init__(self, file):
        self.language = get_language("markdown")
        self.parser = get_parser("markdown")
        self.md_file = Path(file)
        self.md = self.md_file.read_text()
        self.tree = self.parser.parse(self.md.encode())
        self.query = self.language.query(
            f"""
(fenced_code_block
    (info_string) @_info
    (#match? @_info "darkmark")
    (#match? @_info "python")
    (code_fence_content) @darkmark_python
) @darkmark_python_block

(fenced_code_block
    (info_string) @_info (#match? @_info "{DARKMARK_INFO}")
    (code_fence_content)
) @darkmark_output
"""
        )

    @property
    def ip(self):
        try:
            return self._ip
        except AttributeError:
            os.environ["NO_COLOR"] = "1"
            ip = TerminalInteractiveShell.instance()

            ip.extension_manager.load_extension("pyflyby")
            ip.extension_manager.load_extension("rich")
            self._ip = ip
            return ip

    @property
    def node(self):
        self.tree = self.parser.parse(self.md.encode())
        return self.tree.root_node

    def sexp(self):
        return self.node.sexp()

    def captures(self, filter: str = None):
        if filter is None:
            return [
                c for c in self.query.captures(self.node) if not c[1].startswith("_")
            ]
        return [c for c in self.query.captures(self.node) if c[1] == filter]

    def clear(self):
        while self.captures(filter="darkmark_output"):
            capture = self.captures(filter="darkmark_output")[0]
            self.md = replacer.replace_text(self.md, capture, "")

    def run_cells(self):
        console.log("running cells")

        for i in range(len(self.captures(filter="darkmark_python"))):
            capture = self.captures(filter="darkmark_python")[i]
            code = replacer.get_text(self.md, capture)

            out_buffer = io.StringIO()
            err_buffer = io.StringIO()
            sys.stdout = out_buffer
            # sys.stderr = err_buffer
            try:
                console.log(f"running\n{code}")
                self.ip.run_cell(code)
            except Exception as e:
                console.log("hit exception")
                console.log(e)
                sys.stdout = sys.__stdout__
                sys.stdout = sys.__stderr__
                return

            sys.stdout = sys.__stdout__
            sys.stdout = sys.__stderr__

            # get the captured output
            output = out_buffer.getvalue()
            err_buffer.getvalue()

            block = f"\n``` {{.console .{DARKMARK_INFO}}}\n{output}```"

            capture = [
                c
                for c in self.query.captures(self.node)
                if c[1] == "darkmark_python_block"
            ][i]
            self.md = replacer.insert_text(self.md, capture[0].end_point[0] + 1, block)

    def write_text(self):
        self.md_file.write_text(self.md)


if __name__ == "__main__":
    d = DarkMark("test.md")
    d.run_cells()
    print(d.md)
