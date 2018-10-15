# Data Measurements
[return to glossary index](glossary.md)
## These are SBTCVM's measurements for lengths of trits.
	name    | size     | shorthand(s)
	--------+----------+----------
	trit    | 1 trit   | t1  ('t' also used)
	triad   | 3 trits  | t3
	tryte   | 6 trits  | t6  ('T' commonly used)
	nonet   | 9 trits  | t9
	ditryte | 12 trits | t12

Note: in numbered shorthands where n is the number of trits,
it is recommended that (n) be in superscript.

## Kt, Mt, etc.
with the above shorthands, you may find a metric prefix being used with it.
in SBTCVM, this is 1000 units rather than 1024 in binary. eg.
- 1 MT = 1000 KT = 1000000 T (Trytes)
- 1 Mt1 = 1000 Kt1 = 1000000 t1 (trits)
- 1 Mt3 = 1000 Kt3 = 1000000 t3 (triads)
- 1 Mt9 = 1000 Kt9 = 1000000 t9 (nonets)
- 1 Mt12 = 1000 Kt12 = 1000000 t12 (ditrytes)    

SBTCVM used to use 1093 or MPI(7) instead of 1000, but it was both rarely used,
and didn't accomplish anything 1000 can't, so it was changed.
       
measurement examples:    
- SBTCVM has (3^9)*2 or 39366 t9's or 39.366 Kt9's (KiloNonets) of ram
- A 12 trit SBTCVM would have (3^12)*2 or 1062882 t12's, 1062.882 Kt12's (KiloDiTrytes), or approx. 1.06 Mt12's (MegaDiTrytes) of ram.

