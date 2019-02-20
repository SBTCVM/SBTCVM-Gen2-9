# SBTCVM Standard Library
[help index](index.md)

## SSTNPL modules (.stnpmfs & .tas0)

#### comprompt
This is a standard command prompt routine shared by several SSTNPL-based 
programs that need multi-character command line interfaces.

see _shelldemo_ in _demos_ for a good example.

Other notable uses include the **system shell** in **sbtgsh**.

#### cprle
This is a standard decoder for gfxcon's color packart compression method.

see _comppack_ in _demos_ for a good example.

## Assembler modules (.tas0)

#### vdishell
Standard wrapper routine for the as-yet-unfinished SBTVDI disk system
serial shell.

see _VDIBOOT_ in _vmsystem/roms_ for a good example.

## Assembler namespace files (.nsp)