# SBTCVM Mouse
[help index](index.md)

## basic overview:
SBTCVM's pygame frontend features mouse support in all SBTGA modes. 
This document describes its basic usage. 

_CURSES FRONTEND **DOES NOT** SUPPORT THE MOUSE._

_**SSTNPL** usage will be documented when dedicated support is added to it. 
(for now just use inline assembly (via prefixing each assembly line in your SSTNPL source with the `asm` command) using the examples below as reference)_

## plotter:
Mouse coordinates will be aligned to plotter grid.

## TTY:
Mouse coordinates will be aligned to (x0,y0), at the top left character cell.

# assembly usage:

_you may use this in SSTNPL via inline-assembly (`asm`), and variable set (`set`), statements._

### Read a mouse button event:

```
ioread1;>mouse.button

```

### Clear event buffer

_also cleared upon SBTGA mode change._

```
iowrite1;>mouse.button

```

### get x position of last-read event:

```
ioread1;>mouse.lockx
```

### get y position of last-read event:

```
ioread1;>mouse.locky
```

### get current x position:

```
ioread1;>mouse.realx
```

### get current y position:

```
ioread1;>mouse.realy
```
