# SBTCVM xascmd command plugin file specification v1
## Overview:
XAS, being the main build system & external interactive shell of SBTCVM gen2-9,
has plenty of available commands. Most of theses commands are defined in
**.xascmd** files in the **plugins** directory. the following is the format
specification for such **.xascmd** files.


## format structure:
v1 spec xascmd files contains lines split into 4 fields:

	cmd;exec;is_python;takes_arguments

## is_python

- `1` = is a python script
- `0` = is not a python script (**Not yet implemented**)

## takes_arguments

- `1` = arguments will be given to it as specified by the user.
- `0` = no arguments will be passed.



## cmd
This is the command exposed to the xas shell, and xas scripts.

## exec

the Executable command to run.

If is_python field is set to `1`, the exec field is passed to `python`
