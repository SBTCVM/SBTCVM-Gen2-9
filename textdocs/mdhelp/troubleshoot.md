# troubleshooting guide
[help index](index.md)
### the clicalc calculator is not reading decimal input right.
clicalc can only properly recognize numbers from -9841 to +9841. anything less
than -9841 or greater than +9841 _WILL LEAD TO FAULTY INPUT!_

The reason for this is simple: -9841 to +9841 is the range of 9 trits.
in other words, clicalc couldn't tell you if its too big, because reading
the number in the first place requires actually knowing what the number is,
and it can't do that when its outside the 9-trit range, because it can't even
store a number that big, let alone do math with it.

# VMSYSHALT troubleshooting

### I got a VMSYSHALT message! Is this some kind of exception?
Yes, its an exception, but CALM DOWN! normal VMSYSHALT codes:
- __-1__ soft stop. This means the running program requested to shutdown the VM.
- __-50__ User stop. This means YOU requested a shutdown. i.e. Ctrl+C in curses frontend.
- __anything else__ This is possibly a bug. please see the next 3 items.

### Some trom in ROMS caused a VMSYSHALT exception!
bear in mind: the following TROMS there are INTENDED to cause exceptions:
- __excepttest__ Should cause a zero division
- __stacklimittest__ Should cause a stack1 Overflow or stack1 Underflow depending on what was last tested.

### Some trom in APPS caused a VMSYSHALT exception!
Please report this. TROM programs in APPS are intended to be useful, and in fact, 
are not supposed to trigger exceptions.

### Some trom in VMSYSTEM/ROMS (or the default TROM) caused a VMSYSHALT exception!
This should NEVER happen. any TROMs placed here are critical
and must function correctly!!!