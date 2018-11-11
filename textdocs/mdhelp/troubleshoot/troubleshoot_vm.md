# VM troubleshooting
[Troubleshooting Guide Index](troubleshoot.md)

# Q: Why does the pygame frontend have a slower TTY?
Its 600 Characters per second. (CPS) (30 characters max per frame, at 30 FPS)

The reason for this slow speed is mainly to ensure the CPU has enough
processing time to run properly.

## Why 600 CPS?

600 CPS is meant to be a decent enough speed (for a computer running at 6.5Khz with)
without slowing the CPU to a crawl. Any kind of software emulation has its drawbacks,
and number crunching has been placed above text printing in this case.

# Q: Why is curses so limited?
Well It has to do partly with how much terminals in general, even after over half
a century of computing, are not standardized. I know. It's sad, really.

The other thing is terminals obviously don't have much in the way of graphics support.