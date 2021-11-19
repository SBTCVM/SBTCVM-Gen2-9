# SBTCVM Standard Library
[help index](index.md)

Here you will find an overview of the various sorts of libraries and
modules that encompass the SBTCVM standard library.

## SSTNPL modules (.stnpmfs & .tas0)

### segment
This module is used to render vector text on the SBTGA plotter. (mode 30)

see _plottertext_ in _demos_ for a good example.

### dosargs
This is the official SSTNPL module for parsing command line arguments
passed to applications by SBTCVM-DOS's `command.txe`

see the __SBTCVM-DOS source code__ for examples of its usage.

### comprompt
This is a standard command prompt routine shared by several SSTNPL-based 
programs that need multi-character command line interfaces.

see _shelldemo_ in _demos_ for a good example.

Other notable uses include the **system shell** in **sbtgsh** and SBTCVM-DOS's **command shell**.

### cprle
This is a standard decoder for gfxcon's color packart compression method.

see _comppack_ in _demos_ for a good example.

### plrle & plrle_noalpha
This is a standard decoder for gfxcon's compressed tritmap format. (uses SBTGA plotter mode (mode 30, 31))
the latter module name lacks color-key transparency support but is marginally faster when decoding...

see _tritmap_ in _demos_ for a good example.

### binrle
This is a standard decoder for gfxcon's 2-color compressed tritmap format. (uses SBTGA plotter mode (mode 30, 31))
more space-efficient than PLRLE, at a severe cost in image colorspace.

see _`binrle_test`_ in _demos_ for a good example.

### gettriads
A VERY simple module containing a subroutine that extracts the three triads in a nonet, and places them in 3
separate variables....

see _`test_gettriads`_ in _demos_ for usage example.

### mergetriads
Counterpart to `gettriads`, `mergetriads`, as you may suppose, merges 3 triads into a Nonet.

see _`plotter_gradients`_ in _demos_ for usage example.

### strmacro
Basic static named string system via SSTNPL macros. Features output support for `segment` module, standard TTY, and SBTVDI serial commands.

see _`string_macros`_ in _demos_ for usage example.

### rgbadd
A fairly flexible 9-trit RGB color adding library.
Features special modes for incremental-addition-based gradients.

see _`plotter_gradients`_ in _demos_ for usage example.

### musicengine

music playback routine Module for SBTCVM's 4-channel sound chip.

see _musicdemo_ and _ternarydreams_ in _demos_ for good examples.

_ternarydreams_ and _ontrain_ both contain examples of separate music data stored in tas0 files.

Also see counterpart `musnsp.nsp` library for assembler namespace constants for music control code data.

### flocklib

Helps time code around SBTGA's plotter framerate (30FPS).

Wraps `flock.tas0` into a SSTNPL module, while providing a `wait x frames` style function.

see _flock_test_ in _roms_ for a basic test program.


## Assembler modules (.tas0)

### flock

Use inline in a loop of SBTGA Plotter code to 'lock' the code's timing to the plotter's 30FPS framerate.
Extra useful if used with a double-buffer scheme using one of SBTGA's secondary graphics buffers.


### vdishell

Standard wrapper routine for the as-yet-unfinished SBTVDI disk system
serial shell.

see _VDIBOOT_ in _vmsystem/roms_ for a good example.

Also note some programs use VDI commands/make them available using the SBTVDI serial shell's program mode.

## Assembler namespace files (.nsp)

### stdnsp
The standard assembler namespace library

Contains constants for ALL used IOBus addresses. used by nearly every program. including SSTNPL-compiled programs.

### musnsp

Contains music control codes and such for musicengine music data files.