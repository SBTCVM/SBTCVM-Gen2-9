#!/usr/bin/env python
import os
if not os.path.isdir("vmsystem"):
    print("changing to script location...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


import vmsystem.libbaltcalc as libbaltcalc
import sys
import vmsystem.iofuncts as iofuncts
import vmsystem.xaslib as xaslib
# common vars:
xasvers = xaslib.xasvers
versint = xaslib.versint


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
        print('''SBTCVM eXtensible Assembly Script (XAS) v2
For SBTCVM Gen2-9.
help, -h, --help: this help
   -i, [no argument]: run XAS in interactive shell mode.
   -v, --version: SBTCVM XAS version
   -a, --about: about SBTCVM
   -s, --syntax: assembly syntax check mode
   -b, --build (xasname): run xas script.
   (xasname): same as -b/--build''')
    elif cmd in ['-v', '--version']:
        print(xasvers)
    elif cmd in ["-a", "--about"]:
        print('''SBTCVM eXtensible Assembly Script (XAS) v2
''' + xasvers + '''
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
    elif cmd in ["-i"]:
        xaslib.xasshell()
    elif cmd is None:
        xaslib.xasshell()
    elif cmd.startswith("-"):
        print("Unknown option: '" + cmd + "' try xas.py -h for help.")
    else:
        if cmd in ['-b', '--build', '-s', '--syntax']:
            argx = arg
        else:
            argx = cmd
        if cmd in ['-s', '--syntax']:
            syntaxonly = 1
        else:
            syntaxonly = 0
        pathx = iofuncts.findtrom(
            argx,
            ext=".xas",
            exitonfail=1,
            exitmsg="xas file was not found. STOP",
            dirauto=1)
        if xaslib.xasparse(pathx, syntaxonly):
            sys.exit("The script was not run successfully.")
