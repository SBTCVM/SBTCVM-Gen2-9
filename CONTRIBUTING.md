## Overview:

Basic Requirements:
- python 2 & python 3 (python 2 compatibility will be **REQURED** up until its EOL in 2020.
- knodlege of SBTCVM's virtual architecture, its languages, and balanced ternary.

## when you shoud create an issue BEFORE working on somthing:
In order to keep the VM stable, and its compilers working, you should create an issue/check for existing
issues before trying to contribute code, in the following areas:

- ANYTHING in **libtextcon**: This is the refrence implimentation to SBTCVM-GTT2 text encoding! 
Breaking this means **TTY input** AND **TTY output** will break in **ALL** frontends.
Not to mention both the assembler and SSTNPL, and even TROMs can also break.
- CPU code: The CPU runs at 6.5KHz, and is plain python. translation: it needs to be FAST.
- CPU opcodes: Requests for new CPU instructions should be taken up as feature requests. EVEN IF YOU WANT TO DO THE WORK.
- Bundled compilers. SSTNPL and SBTCVM assembly are SBTCVM's only programming languages.
BREAKING COMPATIBILITY WITH OLDER GEN2-9 CODE IS NOT PERMITTED.
