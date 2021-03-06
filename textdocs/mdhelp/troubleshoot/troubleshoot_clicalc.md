# clicalc calculator & memory monitor
[Troubleshooting Guide Index](troubleshoot.md)
# All modes
Known limitation-related issues of the **clicalc** calculator & memory monitor **TROM** found in **APPS**.
### not reading decimal input right
clicalc can only properly recognize numbers from -9841 to +9841. anything less
than -9841 or greater than +9841 _WILL LEAD TO FAULTY INPUT!_

The reason for this is simple: -9841 to +9841 is the range of 9 trits.
in other words, clicalc couldn't tell you if its too big, because reading
the number in the first place requires actually knowing what the number is,
and it can't do that when its outside the 9-trit range, because it can't even
store a number that big, let alone do math with it.

### Results are incorrect

First, if in decimal mode, ensure your inputs were detected correctly (see above).

Also, ensure the result is neither greater than +9841, or vice versa, less than
-9841, else it will have been truncated to that range.

Bare in mind, niether SSTNPL, clicalc, the VM, nor libbaltcalc, have a capacity for
fixed/floating point arithmetic. Hence divisions will be rounded. However modulo
division is provided if you wish to use the remainder for something.

### Why is it limited to 9 trit arithmetic?

Currently, SBTCVM Gen2-9 only is capable of working with 9-trit integers, 
hence the lengthy response to faulty decimal input above, and ternary
input being hard-limited to 9 trits.

# Memory Monitor Mode

### im seeing 'FAULT: the entered address is within clicalc's code memory range!'

Well, clicalc's memory monitor sets aside the area of SBTCVM's RAM that its code resides in, as read-only.

You may, however, write to any IOBUS address, as well as see the writable memory range of RAM via pressing **`m`** at the memory monitor prompt.

### memory range dumping is slow. even in SBTCVM's OS terminal output!

This is done to keep the TTY in the pygame frontend from being overloaded. as SBTCVM's official TTY speed is only 600 character/second. This command is best used with smaller sections of memory...

Please see: **romdump.py**, for a more robust tool.