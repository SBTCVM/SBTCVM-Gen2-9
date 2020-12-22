# Mathematics:
[return to glossary index](glossary.md)
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
The _Maximum Combinations Value_ of a length of trits.
The number of combinations in a length of trits. Formula:

	((3^t))=m       
	Where 't' is the length of trits      
	and 'm' is the MCV of 't'       

## Balanced Septemvigesimal [`Sept`]
Balanced Base 27. this is used for compact representation
of ternary data in text. (_romdump.py's -c option uses this for example_)

sept. digit|decimal value
---|---
D|+13
C|+12
B|+11
A|10
9|+9
8|+8
7|+7
6|+6
5|+5
4|+4
3|+3
2|+2
1|+1
0|0
Z|-1
Y|-2
X|-3
W|-4
V|-5
U|-6
T|-7
S|-8
R|-9
Q|-10
P|-11
N|-12
M|-13
