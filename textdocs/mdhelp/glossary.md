# Technical Glossary
Here is a selection of various terms used in SBTCVM.
_note: This glossary is sorted by category._

# Data Measurements
## These are SBTCVM's measurements for lengths of trits.
	name    | size     | shorthand(s)
	--------+----------+----------
	trit    | 1 trit   | t1  ('t' also used)
	triad   | 3 trits  | t3
	tryte   | 6 trits  | t6  ('T' also used)
	nonet   | 9 trits  | t9
	ditryte | 12 trits | t12

Note: in numbered shorthands where n is the number of trits,
it is recommended that (n) be in superscript.

## Kt, Mt, etc.
with the above shorthands, you may find a metric prefix being used with it.
in SBTCVM, this is 1093 units rather than 1024 in binary. eg.
- 1 MT = 1093 KT = 1194649 T (Trytes)
- 1 Mt1 = 1093 Kt1 = 1194649 t1 (trits)
- 1 Mt3 = 1093 Kt3 = 1194649 t3 (triads)
- 1 Mt9 = 1093 Kt9 = 1194649 t9 (nonets)
- 1 Mt12 = 1093 Kt12 = 1194649 t12 (ditrytes)    
eg.    
- SBTCVM has (3^9)*2 or 39366 t9's or aprox. 36.01 Kt9's (KiloNonets) of ram
- A 12 trit SBTCVM would have (3^12)*2 or 1062882 t12's or approx. 972.44 Kt12's (KiloDiTrytes) of ram

# Mathematics:

## MPI:
The _Maximum Positive Integer_ of a length of trits.
The maximum value a length of trits can store. Formula:

	((3^t)-1)/2=m         
	Where 't' is the length of trits         
	and 'm' is the MPI of 't'        

## MNI:
The _Maximum Negative Integer_ of a length of trits.
The minimum value a length of trits can store.
the absolute value of MNI(9) equals MPI(9),
so the formulas are nearly identical.

## MCV:
The Maximum Combinations Value of a length of trits.
The number of combinations in a length of trits. Formula:

	((3^t))=m       
	Where 't' is the length of trits      
	and 'm' is the MCV of 't'       


# data formats:
## SBTCVM-BTT2
The 9-trit text encoding used by SBTCVM Gen2-9. I.e. in the serial TTY.


# VM Terms:
## VMSYSHALT
A Status message indicating an exit, paired with a status code and a short
description of the exit condition. i.e. divide by zero.