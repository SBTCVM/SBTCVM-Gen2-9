
# XAS Shell/script Commands:

[help index](index.md)

[Main XAS help](xas.md) (NEW USERS: read main XAS help first!)
## Basics

command | arguments | description
:----------:|:--------------:|:-----------:|
xas|(xas script)|Run an xas script.
print|(string)|print text to standard output.
exit|NONE|exit script/shell


## Interactive mode only

command | arguments | description
:----------:|:--------------:|:-----------:|
help|<command>|view help for a command
help|NONE|view list of commands
help|all| list all commands, sorted by category.
ls/list/dir|(path)|list SBTCVM-relevant files in (path)
find|(string)|find filenames containing (string) and list them. **(1)**
ver/version/info|NONE|print version information
about|NONE|about XAS

### Footnote 1

A path without a '+' means its directly visible in SBTCVM's 'path' 

A path with a '+' means its NOT directly visible in SBTCVM's 'path'
In that case, use the '+' path provided.

_Note: This is **NOT** the same as your system's path!_


## VM:
command | arguments | description
:----------:|:--------------:|:-----------:|
run/runp | (same as pyg_sbtcvm.py) | run SBTCVM's Pygame VM Frontend
runc | (same as cur_sbtcvm.py) | run SBTCVM's Curses VM Frontend

## Build


command | arguments | description
:----------:|:--------------:|:-----------:|
asm| (same as g2asm.py) | run assembler
stnp| (same as stnpcom.py) | run SSTNPL compiler

## Debugging

commad | arguments | description
:----------:|:--------------:|:-----------:|
dump|(same as romdump.py)|TROM dump utility


### Romdump Macors
command | arguments | description
:----------:|:--------------:|:-----------:|
trominfo|(trom image)|get some basic info on a trom. i.e. size.
dumpnp|(trom image)| Dump TROM image (n0p syntax)
vdump|(trom image)| Dump  TROM image in verbose format
vdumpnp|(trom image)| Dump  TROM image in verbose format (n0p syntax)
sdump|(trom image)| Dump strings from TROM image
t0dump|(trom image)| dump raw character data from data words.
t1dump|(trom image)| dump raw character data from instruction words.


