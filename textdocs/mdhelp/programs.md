# SBTCVM Gen2-9's Programs
[help index](index.md)

# VM Frontends

**BOTH** frontends feature sound emulation when a sound backend is found. _pygame only at this time_

(pygame frontend recommended)



### PYG_SBTCVM.py: (PYGAME) [XAS command: run/runp]
_requires pygame (truetype font and PNG support **REQUIRED**)_


SBTCVM's virtual machine. (with pygame frontend)


Features an, 81-column by 25-line color graphical TTY display, SBTGA Graphics, mouse, and sound.


### CUR_SBTCVM.py: (CURSES) [XAS command: runc]
SBTCVM's virtual machine. (with curses frontend)

_Note: Curses Frontend is **BUGGY**_

Note: XAS-related CTRL+C bug has been fixed.

note: recommended to use terminal thats 81 columns or wider.

also, the curses frontend may lack certain features. i.e. graphics.

Does feature sound when pygame is installed.


# Development Tools & Compilers

### xas.py: [XAS command: xas]
SBTCVM's eXtensible Assembly Script, or XAS, is in charge of scripting
together complex build processes of more complex applications and 
components. Though many TROM programs lack need for it, and so use
stnpcom.py or g2asm.py directly. Note: the "xas" xas command runs XAS scripts.

It also features an interactive mode with some extra commands. Just run `xas.py` with no arguments, in a terminal.




### g2asm.py: [XAS command: asm]
SBTCVM's assembler. Not only does it act as SBTCVM's lowest level language, i
t also acts as a target for other programming
languages, like SSTNPL. Helps to have a grasp of balanced ternary and how
lower level programming works.


### stnpcom.py: [XAS command: stnp]
The SSTNPL compiler. While not as efficient as the assembler, SSTNPL is a powerful, static language.

Containing a more familiar variable system, a (static sized) 2-axis table (array) interface,
iterators, several conditional comparisons and operations, and a myraid of IO macros, and
other powerful features. 

Includes a module system with proper "module.var" namespace separation.
When used, the SSTNPL compiler will automatically run the assembler for you.


### diskedit.py: [XAS command: diskedit]
disk edit & build utility for SBTCVM's disk image format.
can generate disk images from *.diskmap files.


### romdump.py: [XAS command: dump]
An advanced debug tool. works with TROMS and VDI disk files.
works as an equivalent to 'hexdump' and 'strings', as well as other
features. such as disk filelist viewing.

### gfxcon.py: [XAS command: gfxcon]
Assorted graphics conversion functions. 
note: requires pygame.
