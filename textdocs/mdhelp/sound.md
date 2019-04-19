# SBTCVM Sound Chip (SBTSND-1000)
[help index](index.md)




## Features:

- 4 voices (channels)
- each voice has: square, sawtooth, triangle, noise, square-pulse, and triangle-pulse.
- Stereo (left, right, center) panning support.
- per-channel volume.

## examples:
- see 'sounddemo' in 'demos' for a set of basic tests/example code.
- see 'musicdemo' in 'demos' for a demo of SBTCVM's musicengine SSTNPL module.

## Technical Notes:

- waveform synthesis works via looping a computed sample of the target waveform, 
generated with the desired frequency, (and if applicable, pulse width)
- waveform synthesis is performed each time frequency, pulse, or waveform is changed.
- the waveform algorithms are provided by fssynthlib. you can find its
readme in the textdocs directory.
