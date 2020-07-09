# SBTCVM XAS script/shell help.
[help index](index.md)

[XAS commands](xas_com.md)

# basic syntax:
`command;arg`


**OR:**

`command arg`

_You should use a ';' if your print argument contains one!!!_

**For example:**


	print hello
	xas somescript.xas
	exit


**Is identical to:**


	print;hello
	xas;somescript.xas
	exit


# '+' Path syntax:
Given that SBTCVM is meant to be portable, XAS uses a special operator for path delination:

For example say we have a TROM APP directory called `SOMEAPP` in `VMUSER`, and we have our
`auto_main.xas` file call a secondary xas script we have there. picture it looking like so:


	auto_main.xas
	something.xas


Since `something.xas` is not the 'auto' xas (prefixed with `auto_`), we need to
tell XAS its NOT in the main search path. **(`APPS, DEMOS, VMSYSTEM, VMSYSTEM/ROMS, ROMS, VMUSER` and `r_*` directories within them)**

As `SOMEAPP` is in `VMUSER`, aka in the search path, we only need:


	xas SOMEAPP+somthing.xas


similar for 'non-auto' stnp and tasm files.

This syntax is also supported in other parts of SBTCVM. such as the VM's TROM argument, and the compilers.

## On TROM APP directories:

When using the xas shell's find and list/ls/dir commands, you will sometimes
see a directory, being listed as multiple types:


	------listing of: 'APPS'
	   Directory  : clicalc
	       SSTNPL     : clicalc
	       Rom Image  : clicalc



This basically means you can type that directory's name, i.e. `clicalc` in 
the example, as an argument for that SBTCVM filetype.

Whats going on here, is the directory contains a file of that type, prefixed with **`auto_`**
i.e.
**`auto_main.trom`**

## XAS-script-specific features:

### script location shorthand

	print %xwd%
	stnp %xwd%+somthing.stnp

`%xwd%` is a XAS-script-specific shorthand that automatically fills in 
the current XAS script's location in its place.

it can definately help larger projects.

it is _NOT SUPPORTED_  **_ANYWHERE_** ELSE!

