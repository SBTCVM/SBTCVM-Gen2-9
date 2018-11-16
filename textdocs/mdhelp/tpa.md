# Ternary-Packed art
[help index](index.md)

Ternary-packed art is a hardware-supported encoding scheme for rendering sets
of 9 'pixel' values, encoded as 1 Nonet (data word) each, to the TTY.

also see the 27-color variant: [Color Ternary-Packed art](ctpa.md)


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
`+`|White
`0`|Grey
`-`|Black

Default colors can be changed. for more information see [TTY colors](tty_colors.md)

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

have a look at `packtest2` and `packtest3` in `DEMOS` for a simple example.

## other ways:
You can also just specify it using raw strings of 9 trits if your doing something fancy.