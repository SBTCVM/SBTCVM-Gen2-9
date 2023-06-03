#!/usr/bin/env python

import os
if not os.path.isdir("vmsystem"):
    print("changing to script location...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


import vmsystem.libbaltcalc as libbaltcalc
import sys
import vmsystem.iofuncts as iofuncts
import vmsystem.libstbxpl as stbxpl
# from vmsystem.g2asmlib import mainloop


compvers = stbxpl.compvers
versint = stbxpl.versint

print("THIS COMPILER IS NOT FINISHED!\nIt is not yet able to produce proper TROMs and TXE disk programs.")


if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
    except BaseException:
        cmd = None
    try:
        arg = sys.argv[2]
    except BaseException:
        arg = None
    if cmd in ['help', '-h', '--help']:
        print('''SBTCVM Ternary Blocked eXstensible Programming Language
--For SBTCVM Gen2-9.
   help, -h, --help: this help
   -v, --version: sxtbpl compiler version
   -a, --about: about SBTCVM
   -c [sourcefile], --compile [sourcefile]: Compile source file into a tasm
      file, then run the assembler on it automatically, if successful.
   [sourcefile]: same as -c''')
    elif cmd in ['-v', '--version']:
        print(compvers)
    elif cmd in ["-a", "--about"]:
        print('''SBTCVM Ternary Blocked eXstensible Programming Language
''' + compvers + '''
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

Copyright (c) 2016-2022 Thomas Leathers and Contributors

see readme.md for more information and licensing of media.

  SBTCVM Gen2-9 is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  SBTCVM Gen2-9 is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with SBTCVM Gen2-9. If not, see <http://www.gnu.org/licenses/>

  ''')
    elif cmd is None:
        print("Tip: Try stbxpl.py -h for help.")
    elif cmd.startswith("-") and cmd not in ['-c', '--compile']:
        print("Unknown option: '" + cmd + "' try stbxpl.py -h for help.")
    else:
        if cmd in ['-c', '--compile']:
            argx = arg
        else:
            argx = cmd
        pathx = iofuncts.findtrom(
            argx,
            ext=".stbxpl",
            exitonfail=1,
            exitmsg="stbxpl file was not found. STOP",
            dirauto=1)
        stbxpl.parse(pathx)
