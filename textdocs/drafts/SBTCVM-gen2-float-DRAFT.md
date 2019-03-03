# SBTCVM Gen2-9 Ternary Floating Point Implementation plan (DRAFT)

## Overview

The basic principle here is storing the significand
and the exponent of a balanced ternary float separately in 2 9-trit half-words:


## Basic Formula
(*)=refers to a single-letter shorthand to be used in formulas within this document

inst=exponent(E)
data=significand(S)

### Formula:

S*3^E


## Examples
using this formula, we can determine that:

1*3^-1=.3333333333333333333333... (repeating)

and:

1*3^1=3


## Range

to determine how large a number we can represent we can use the following:

##### 9 by 9 floating point Max Positive Float (MPF):

9841*(3^9841)

##### 9 by 9 floating point Max Negative Float (MNF):

-9841*(3^9841)

## CPU opcodes & memory storage plan


instructions within the CPU will be implemented as double-word instructions such as:

inst|data
:----|---:
main opcode|subcode
exponent **(E)**|significand **(S)**

furthermore, each floating point operation will be implemented as a 'subcode' under a master opcode.