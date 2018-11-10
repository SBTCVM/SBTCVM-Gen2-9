# Ternary-Packed art
[help index](index.md)

Ternary-packed art is a hardware-supported encoding scheme for rendering sets
of 9 'pixel' values, encoded as 1 Nonet (data word) each, to the TTY.

## Why?

 - its 9-times smaller than (rectangular) text art of the same size.**(1)**
 - in graphical frontends, it shows as blocks of color.
 - in curses, it shows as 'ascii art.'

##### footnotes:

1. Width is must be padded to multiple of 9, due to encoding constraints.

## pygame frontend:
In the pygame frontend, they use the following colored-block scheme:

trit|printed as
---|---------
`+`|White **(1)**
`0`|Grey **(1)**
`-`|Black **(1)**

1. tinted slightly blue with default colors.

## curses, standard output, logs

In curses, standard output, and the logs, the following scheme is used:

trit|printed as
---|---------
`+`|`#`
`0`|`-`
`-`|(space)

## how to (images)

To encode art in this way, you can use `gfxcon.py -p [image]`, and it will
generate a `tas0` file for you to include. output is SSTNPL-friendly

_(overrides `fop1` and `fop2`, so you may need to reset those if not using SSTNPL_

**note:** `gfxcon.py` requires pygame in order to process images, and will
refuse to run should it be missing.

have a look at `packtest2` in `DEMOS` for a simple example.

## other ways:
You can also just specify it using raw strings of 9 trits if your doing something fancy.