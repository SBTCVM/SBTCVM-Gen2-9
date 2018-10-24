# Data Measurements
[return to glossary index](glossary.md)
## These are SBTCVM's measurements for lengths of trits.

name    | size     | short  | (alt 1) | (alt 2)
:-------|:---------|:----- -|:----:|:----:
trit    | 1 trit   | t1     | t^1  | t
triad   | 3 trits  | t3     | t^3  | 
tryte   | 6 trits  | t6     | t^6  | T
nonet   | 9 trits  | t9     | t^9  | 
ditryte | 12 trits | t12    | t^12 | 

**Note:** _In numbered shorthands (shorthands with the form **t(n)**,
it is recommended that **(n)** be in superscript when possible, as shown in **(alt 1)**._

## Kt, Mt, etc.
With the above shorthands, you may find a metric prefix being used with it.
in SBTCVM, this is _1000_ units rather than _1024_ in binary. eg.

- 1 MT = 1000 KT = 1000000 T (Trytes)
- 1 Mt1 = 1000 Kt1 = 1000000 t1 (trits)
- 1 Mt3 = 1000 Kt3 = 1000000 t3 (triads)
- 1 Mt9 = 1000 Kt9 = 1000000 t9 (nonets)
- 1 Mt12 = 1000 Kt12 = 1000000 t12 (ditrytes)    

**Note: **_SBTCVM used to use 1093 or MPI(7) instead of 1000, but it was both rarely used,
and didn't accomplish anything 1000 can't, so it was changed._

### measurement examples:    
- SBTCVM has (3^9)*2 or 39366 t9's or 39.366 Kt9's (KiloNonets) of ram
- A 12 trit SBTCVM would have (3^12)*2 or 1062882 t12's, 1062.882 Kt12's (KiloDiTrytes), or approx. 1.06 Mt12's (MegaDiTrytes) of ram.

