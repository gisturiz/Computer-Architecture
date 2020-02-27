#!/usr/bin/env python3

"""Main."""

import sys

from cpu import *

cpu = CPU()
branch_table = BranchTable()

cpu.load(sys.argv[1])
cpu.run()
#branch_table.run()
