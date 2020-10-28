# data formats:
[return to glossary index](glossary.md)
## SBTCVM-BTT2

The 9-trit text encoding used by SBTCVM Gen2-9. I.e. in the serial TTY.

## TROM

SBTCVM's memory image format. can be run via one of the VM frontends.    
`romdump.py` can be used to view their contents in a hexdump-style fashion.

## TDSK1

SBTCVM's ternary floppy disk image format.
`romdump.py` and `diskedit.py` are relevant here.

## TXE

A full-memory 'raw' executable format used on SBTCVM SBTVDI disk drives, notably in SBTCVM-DOS.

## CPRLE

A Run-length compressed variant of 27-color pack-art. requires a dedicated
decoder.
takes the form:

inst|data|info
----|----|----
1|`+++---00+`|write color packart in **data**, **2** times.
0|`++-+++000`|same as above, but only **1** time.
-1|**N/A**|print a newline (used for formatting)

also, the **first word** of the image data contains the **end address** in its data word.

## PLRLE

A decendant of CPRLE, PLRLE is an advanced, **9-trit RGB tritmap compression format**,
complete with lossy & lossless compression modes, and a combined decoder/renderer 
with basic scaling support. works with the **SBTGA** Plotter (mode 30, 31)

## BINRLE

like PLRLE, its a Run-length tritmap compression format for the SBTGA plotter(mode 30, 31)
the key difference is a lack of a lossy compression mode, and a hard-limit of only 2 colors.

interpolation mode can be used to emulate a tone between the two colors, to an extent.
