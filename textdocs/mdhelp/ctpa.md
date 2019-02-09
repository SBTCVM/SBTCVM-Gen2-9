# Color Ternary-Packed Art
[help index](index.md)

## Whats the difference from normal T.P.A.?
Instead of 9 `pixels` of a 3-color palette, Color ternary Packed art uses 3,
3-trit RGB color values directly, to output 3 `pixels` at once.

## This doesn't work in curses does it?
Does not work in curses, whatsoever!

Mainly, its due to the lack of any non-color data that can be properly displayed.

## basic howto:

Assembly:

	setreg1;+---+---+
	iowrite1;>io.cpack

SSTNPL:

	cpack *+---+---+
	cmulpk +++---+++;---+++---;+++000+++
	clinepk +++---+++;---+++---;+++000+++
	cmulpk +++---+++;---+++---;+++000+++;+++000+++
	clinepk +++---+++;---+++---;+++000+++;+++000+++


**clinepk**, like **cmulpk**, is a handy batch-macro for fixed 27 color ternary
packed art values. The difference is it outputs a newline automatically.


## Examples?

You should check `colorpack` in `DEMOS`. it also has examples of
SSTNPL's cmulpk and clinepk commands.

# compression

a compressed variant is available via gfxcon -cprle(n).

Needs to be decoded via algorithm. `comppack` in `demos` features a basic decoder.