# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
from IPython.core.magic import Magics, line_magic, magics_class

from darkmark.darkmark import DarkMark


@magics_class
class DarkMarkMagics(Magics):
    @line_magic
    def drun(self, line):
        file = line.strip()
        d = DarkMark(file)
        d.run_cells()
        return d


def load_ipython_extension(ipython):
    ipython.register_magics(DarkMarkMagics)
