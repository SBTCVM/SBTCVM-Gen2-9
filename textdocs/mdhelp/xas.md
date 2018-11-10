# SBTCVM XAS script/shell help.
[help index](index.md)


# basic syntax:
`command;arg`


**OR:**

`command arg`

_You should use a ';' if your print argument contains one!!!_

**For example:**

```
print hello
xas somescript.xas
exit
```

**Is identical to:**

```
print;hello
xas;somescript.xas
exit
```

# '+' Path syntax:
Given that SBTCVM is meant to be portable, XAS uses a special operator for path delination:

For example say we have a TROM APP directory called `SOMEAPP` in `VMUSER`, and we have our
`auto_main.xas` file call a secondary xas script we have there. picture it looking like so:

```
auto_main.xas
something.xas
```

Since `something.xas` is not the 'auto' xas (prefixed with `auto_`), we need to
tell XAS its NOT in the main search path. **(`APPS, VMSYSTEM, VMSYSTEM/ROMS, ROMS, VMUSER` and r_* directories within them)**

As `SOMEAPP` is in `VMUSER`, aka in the search path, we only need:

```
xas SOMEAPP+somthing.xas
```

similar for 'non-auto' stnp and tasm files.

This syntax is also supported in other parts of SBTCVM. such as the VM's TROM argument, and the compilers.

# Commands:

## Basics

commad | arguments | description
:----------:|:--------------:|:-----------:|
xas|(xas script)|Run an xas script.
print|(string)|print text to standard output.
exit|NONE|exit script/shell


## Interactive mode only

commad | arguments | description
:----------:|:--------------:|:-----------:|
help|(category)|view help category
help|all|view all help categories
help|list|view a list of help categories.
ls/list/dir|(path)|list SBTCVM-relevant files in (path), in valid XAS '+' path syntax.
find|(string)|find filenames containing (string) and list them with their valid XAS '+' path syntax.


## Build


commad | arguments | description
:----------:|:--------------:|:-----------:|
asm| (same as g2asm.py) | run assembler
stnp| (same as stnpcom.py) | run SSTNPL compiler

## Debugging

commad | arguments | description
:----------:|:--------------:|:-----------:|
dump|(same as romdump.py)|TROM dump utility

### Romdump Macors
commad | arguments | description
:----------:|:--------------:|:-----------:|
trominfo|(trom image)|get some basic info on a trom. i.e. size.
dumpnp|(trom image)| Dump TROM image (n0p syntax)
vdump|(trom image)| Dump  TROM image in verbose format
vdumpnp|(trom image)| Dump  TROM image in verbose format (n0p syntax)
sdump|(trom image)| Dump strings from TROM image
t0dump|(trom image)| dump raw character data from data words.
t1dump|(trom image)| dump raw character data from instruction words.




