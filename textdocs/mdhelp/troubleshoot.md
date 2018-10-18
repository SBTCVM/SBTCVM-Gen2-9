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