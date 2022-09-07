# VM troubleshooting FAQ
[Troubleshooting Guide Index](troubleshoot.md)

Troubleshooting guide for common VM problems and limitations.

# Q: I tried musicdemo or sounddemo but didn't hear anything!

# A: currently, while all frontends enable the sound emulation,
the sound emulation requires pygame. even when you aren't using
the pygame frontend. Also, ensure your Operating System hasn't
muted the program in some way.

# Q: Why does the pygame frontend have a slower TTY?
Its 2700 Characters per second. (CPS) (90 characters max per frame, at 30 FPS)

## Why 2700 CPS?

Originally It was 900 CPS but this was found to be far lower than it really needed
to be performance-wise, particularly when considering the often intermittent
nature of the TTY's output in general.

# Q: Why is curses so limited? Why no colors?
Well It has to do partly with how much terminals in general, even after over half
a century of computing, are not standardized. I know. It's sad, really.

The other thing is terminals obviously don't have much in the way of graphics support.
and displaying 27-color, 3-trit RGB would require some rather uncommon
ANSI escape sequences.
