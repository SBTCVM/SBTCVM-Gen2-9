# welcome
[help index](index.md)
### Overview:
SBTCVM Is a project to develop balanced ternary virtual machines and related tools and languages. SBTCVM gen 2-9 is the latest and greatest of that effort, and its no pipe dream. Its real, working, code. 

### Balanced Who?

balanced ternary. 3 values: Positive (`+`), Zero/Ground (`0`), and Negative (`-`)
Its a bit of an oddball system. Its inherently signed, and 2 is actually `+-`,
Not `+0`, which is actually 3. `-+` and `-0` are -2 and -3 respectively.

You might think balanced ternary is some new idea trying to replace binary. 
_New_, however, is not the correct term, and SBTCVM isn't even the first
virtual implementation. I won't bore you with a history lesson here,
but do look it up if your interested, its quite interesting.

### so what does SBTCVM do exactly?
The 'VM' in SBTCVM referees to SBTCVM's virtual implementation of a balanced
ternary computer.  Its written in python, so its not the fastest thing in the
world (6.5KHz CPU), but it does have:

- 19,683 words or, 39.366 KN (KiloNonets [GLOSSARY](glossary/glossary_datameasure.md) ), of RAM
- an assembler
- and SSTNPL, a nice higher-level language. (higher-level than the assembler at least.)

### What are the SBTCVM project's goals?
- provide a stepping stone for those venturing into the world of balanced ternary.
- provide a capable, portable, virtual machine, with development tools, and programming languages.
- help bring balanced ternary computing into the 21st century.






