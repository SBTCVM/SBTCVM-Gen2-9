# SBTCVM Gen2-9
Simple Balanced Ternary Computer Virtual Machine     
     
v2.1.0.alpha    

**Need Help? [See our Getting started guide](/guide.md)**

[SBTCVM Project blog](https://sbtcvm.blogspot.com/)


## What is SBTCVM?

Ever wonder what computers other than the boring-old binary would be like? Well, look no further!
SBTCVM, a python-written VM, simulates the little-known base number called Balanced Ternary!

What is balanced ternary? well, it has "0" and "+1", just like binary, 
but added into the mix is a "-1"! Yes, this means EVERY number is signed. 

Intrigued? Well, as
SBTCVM is Free & Open Source Software, and comes with a ready-to-use
set of compilers and development tools, Getting started with balanced 
ternary with SBTCVM, should prove a fun challenge!

## Features:
- bundled ternary software. including demos, games and utilities.
- 4 channel sound chip
- 6.5Khz, 9-trit CPU
- 39.388 KiloNonets of system RAM
- pygame frontend features color graphics.
- multiple specialized programming languages with integrated compilers. (SSTNPL, SBTCVM assembly)
- Suite of development tools and utilities.
- cross-platform interactive shell and build system. (xas.py)

### Dependencies:
Python __2.7__ OR __3__.

**Sound (all frontends) (powered by FSSynthlib):** pygame

**gfxcon.py:** pygame (used to process images)

**Curses VM frontend:** curses

**Pygame VM frontend:** pygame _**(needs truetype font and PNG support!)**_

## Install instructions:

1. Ensure python is installed.
2. Ensure pygame and curses are installed for your system's default python installation.
3. keep downloaded files in a place you can easily access.
4. **DO NOT** try to move/change the default directory structure!
5. proceed to the [Getting started guide](/guide.md)


## Filing bug reports

**SBTCVM _Should in theory_ work in any Operating system with  python (2.7 or 3), pygame, and curses.**     
If it does not, or you have hit some other sort of bug, please file a bug report stating your 

 - python version
 - pygame version
 - Operating system
 - along with a description of the problem.

 
**Note:** please consult the [Troubleshooting guide](/textdocs/mdhelp/troubleshoot/troubleshoot.md)
 BEFORE filing a bug report!


at the [SBTCVM Gen2-9 issue tracker on github.](https://github.com/SBTCVM/SBTCVM-Gen2-9/issues)
_Please try and read though existing issues to see if its a known bug._

## notes for linux software packagers:

- **SBTCVM** is **SINGLE USER**
- The official name of this specific version of the SBTCVM Suite is: `SBTCVM Gen2-9`
- The user needs access to the `vmuser` directory.
- any desktop entries should include one that starts the **XAS shell** (run `xas.py` with no arguments) in a terminal emulator.
- the python executables & utilities **ARE NOT** designed to be used from arbitrary directories. further they will all change their working directory to their location automatically.
- the official, current, SBTCVM icon can be found in `vmsystem/GFX`



## Code Licensing

SBTCVM gen2-9 ships with **fssynthlib.py**, a general-use waveform synthesis library from
the FSSS synthesizer suite. You can find its readme in the [textdocs directory.](/textdocs/fssynthlib_README.md)
     
Copyright (c) 2016-2019 Thomas Leathers and Contributors 


  SBTCVM Gen2 9-trit is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Gen2 9-trit is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Gen2 9-trit. If not, see <http://www.gnu.org/licenses/>

## licensing For images and media below

all images and other media content, unless otherwise noted,
are licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

Image and other media content created by, (unless otherwise noted below) Thomas Leathers.

SBTCVM's Stylized text logo and SBTCVM's 3 eyed, 3 eared mascot were created by Thomas Leathers.
Copyright (c) 2018 Thomas Leathers and Contributors.
