 
# SBTCVM Assembly v3.x Documentation

**special note:** this is incomplete, also see `opcodes.txt` and `iobus.txt`
in parent directory...

## Introduction

SBTCVM Assembly v3, also known as `G2ASM` or `tasm`, Is an advanced
listing-style assembler for the SBTCVM Gen2-9 virtual machine.

# Basic Syntax

## normal keywords

a normal keyword is for the most part any keyword that translates to a CPU Opcode.  
Normal keywords support the following argument types:

#### Ternary Integers

two notations are supported `+0-` and `p0n` notations. up to 9 trits
may be specified.

	setreg1;+++---000
	setreg2;pppnnn000


#### Decimal Values

In order to use decimal values you must prefix them with `10x` similar to `0x`
when working with hexadecimal numbers in many binary languages.

	setreg1;10x12
	setreg2;10x-12



#### Character Values

use character values. any plain character supported by SBTCVM-BTT2 encoding
can be used when prefixed via a `:` (colon).


	setreg1;:C


the following characters require escape sequences:

ASCII        | escape sequence in assembly
-------------|----------
newline      | `\n`
null         | `\0`
backspace    | `\x`
vertical bar | `\v`
`;`          | `\c`
`\`          | `\\`
space        | `\s`
`#`          | `\p`
`,`          | `\m`


#### Namespace variable references

(see Next Section for what these are...)


	setreg1;>my_namespace_var
	goto;>my_label


# Namespace Variables

## Labels

any normal keyword can be given a label by appending one via
a second semicolon `;`


	setreg1;10x1;my_label



## custom namespace variables

you can create your own namespace variables from raw values like this:


	v>my_namespace_var;10x0
	v>another_one;+0-
	v>and_yet_another;:R



