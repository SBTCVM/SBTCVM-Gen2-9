# SBTCVM Ternary SBTVDI Disk Format 1 Specification

## Overview:

The tdsk1 format was designed for use with SBTCVM Gen2-9's SBTCVM Virtual Disk Interface (SBTVDI).

## Header:

The header contains 2 fields, on the first and second line:

	Disk name
	2

The first line, `Disk name` refers to a plaintext disk label. should be a short description. i.e. `SBTCVM-DOS`

The second line should match the number of files in the tdsk1 image. this **IS** used in part to detect corrupted disk images, so it **MUST BE SET CORRECTLY.** Here, it says the disk contains 2 files.


## File size:
The TDSK1 specification could support files up to 531441 words long (1,062,882) Nonets, **TECHNICALLY.**
though its recommended to keep disk files at a reasonable size.

Applications will need to obviously fit within SBTCVM's 9-trit memory (19,683 words, OR 39,366 Nonets

## File count:
a TDSK1 image may have no more than 9841 files.

## Seeking within files:
The files are seeked using a 12-trit integer. split into 2 Nonets:

- Bank (3-trits)
- bankline (9-trits)

