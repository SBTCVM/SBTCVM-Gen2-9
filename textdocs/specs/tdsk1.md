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
The TDSK1 specification supports files up to 19,683 Words long. (OR 39,366 Nonets)

## File count:
a TDSK1 image may have no more than 243 files.

## Seeking within files:
The files are seeked using a 9-trit integer.
Reverse indexing is not available.

## misc:
Max amount of raw file data: 9.5MegaNonets
Rough Disk size: ~50MB max. (WILL BE SMALLER IN MOST CASES!)
