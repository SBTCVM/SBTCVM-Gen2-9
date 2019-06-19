# data formats:
[return to glossary index](glossary.md)
## SBTCVM-BTT2

The 9-trit text encoding used by SBTCVM Gen2-9. I.e. in the serial TTY.

## TROM

SBTCVM's memory image format. can be run via:      
`./SBTCVM_G2_9.py maze`      
Where 'maze' is an example of a trom name.      
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
