# SBTCVM Ternary ROM image (TROM) specification v3
## Overview:
Gen2, among many other changes, has dropped the old ternary-string based TROM 
format (of specs v1 and v2), and has adopted the following format for TROM 
specification v3

## format structure:

	instruct,data
	instruct,data
	instruct,data
	...

#### example:

	-9459,1
	-9457,5
	0,0

## instruct & data constraints:

- these should be in signed decimal integer form
- they should not exceed the range of possible values in 9-trits: No higher
than +9841, and now lower than -9841.

## sizes:
TROM files may contain anywhere from 1 to 19,683 instruct,data pairs.