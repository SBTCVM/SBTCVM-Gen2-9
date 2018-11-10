# SBTCVM Gen2-9's Programs
[help index](index.md)

# VM Frontends

### SBTCVM_G2_9.py: (CURSES)
SBTCVM's virtual machine. (with curses frontend)

This version must be run in a terminal! 

also, the curses frontend may lack certain features. i.e. graphics.

### PYG_SBTCVM.py: (PYGAME)
SBTCVM's virtual machine. (with pygame frontend)

Features an, 80-column by 25-line graphical TTY display, and launch-from-xas integration that isn't buggy.


# Development

### g2asm.py:
SBTCVM's assembler. Not only does it act as the primary language SBTCVM's
VM is programmed with, it also acts as a target for other programming
languages, like SSTNPL. Helps to have a grasp of balanced ternary and how
lower level programming works.

### xas.py:
SBTCVM's eXtensible Assembly Script, or XAS, is in charge of scripting
together complex build processes of more complex applications and 
components. Though many TROM programs lack need for it, and so use
stnpcom.py or g2asm.py directly.

It also features an interactive mode with some extra commands.



### stnpcom.py:
the SSTNPL compiler. This is the ideal way to learn balanced ternary math,
along with a bit of programing too. Ideal for beginners. for more serious
algorithms, you may find the assembler better suited.
When used, the SSTNPL compiler will automatically run the assembler for you.

### romdump.py:
A nifty SBTCVM trom dump utility with 2 formatting modes and 2 trit
representations. akin to unix/linux 'hexdump' command.

### gfxcon.py:
Assorted graphics conversion functions. 
note: requires pygame.
