# TTY color support help
[help index](index.md)

If you checked out `colortext` and `packtest3` in the pygame frontend, you may be
wondering where those fancy colors come from.

## What about curses?
Well, its not supported. curses will display the uncolored text and ternary
packed art however...

## ternary packed art colors?
Due to the inherent 9-pixel chunks it uses, you can only change colors,
at most, on each of those boundaries.

The following assembly code will change the default colors to a bright blue (`-0+`)
color for `+`, a dark cyan (`--0`) for `0` and black (`---`) for `-`

SBTCVM ASM v3:
	setreg1;-0+-00---
	iowrite1;>io.packcolor

SSTNPL:
	packcolor *-0+-00---

## Text color?

The following assembly code will change the text Foreground color to bright cyan (`0++`)
and the text Background color to dark blue (`--0`).

SBTCVM ASM v3:
	setreg1;0++--0
	iowrite1;>io.textcolor

SSTNPL:
	textcolor *0++--0

## What color palette do these use?
Well, its no arbitrary palette, its actually 3-trit RGB.

For each channel:

ternary|binary
:--:|:----:
`+` |255
`0` |127
`-` |0


## Examples?

You can find `colortext` and `packtest3` in `DEMOS`.