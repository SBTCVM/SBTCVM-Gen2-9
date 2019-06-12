# SBTCVM Gen2-9's Programs
[help index](index.md)

# VM Frontends

**BOTH** frontends feature sound emulation when a sound backend is found. _pygame only at this time_

(pygame frontend recommended)



### PYG_SBTCVM.py: (PYGAME) [XAS command: run/runp]
_requires pygame (truetype font and PNG support **REQUIRED**)_


SBTCVM's virtual machine. (with pygame frontend)


Features an, 81-column by 25-line color graphical TTY display, SBTGA Graphics, mouse, and launch-from-xas integration that isn't buggy.


### CUR_SBTCVM.py: (CURSES) [XAS command: runc]
SBTCVM's virtual machine. (with curses frontend)

_Note: Curses Frontend is **BUGGY**_

Note: XAS-related CTRL+C bug has been fixed.

note: recommended to use terminal thats 81 columns or wider.

also, the curses frontend may lack certain features. i.e. graphics.


# Development

### g2asm.py: [XAS command: asm]
SBTCVM's assembler. Not only does it act as the primary language SBTCVM's
VM is programmed with, it also acts as a target for other programming
languages, like SSTNPL. Helps to have a grasp of balanced ternary and how
lower level programming works.

### xas.py: [XAS command: xas]
SBTCVM's eXtensible Assembly Script, or XAS, is in charge of scripting
together complex build processes of more complex applications and 
components. Though many TROM programs lack need for it, and so use
stnpcom.py or g2asm.py directly. Note: the "xas" xas command runs XAS scripts.

It also features an interactive mode with some extra commands.

### diskedit.py: [XAS command: diskedit]
disk edit & build utility for SBTCVM's disk image format.
can generate disk images from *.diskmap files.

### stnpcom.py: [XAS command: stnp]
the SSTNPL compiler. This is the ideal way to learn balanced ternary math,
along with a bit of programing too. Ideal for beginners. for more serious
algorithms, you may find the assembler better suited.
When used, the SSTNPL compiler will automatically run the assembler for you.

### romdump.py: [XAS command: dump]
An advanced debug tool. works with TROMS and VDI disk files.
works as an equivalent to 'hexdump' and 'strings', as well as other
features. such as disk filelist viewing.

### gfxcon.py: [XAS command: gfxcon]
Assorted graphics conversion functions. 
note: requires pygame.
