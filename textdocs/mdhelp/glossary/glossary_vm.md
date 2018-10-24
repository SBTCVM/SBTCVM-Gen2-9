# VM Terms:
[return to glossary index](glossary.md)

Terms related to the VM, and the backend that makes it work.
## VMSYSHALT
A Status message indicating an exit, paired with a status code and a short
description of the exit condition. i.e. divide by zero.

## VMSYSTEM
This is where SBTCVM's backend code, standard library, and system-related TROMs are kept.

## libbaltcalc
SBTCVM's powerful Balanced Ternary mathematics library, which provides the
function/string based API used by prior "Gen 1" SBTCVM versions, and the newer
btint object API used by SBTCVM Gen2-9.

libbaltcalc is developed separately from SBTCVM itself. You can find the
repo on the SBTCVM project github:

[libbaltcalc repo](https://github.com/SBTCVM/libbaltcalc)

## btint
A class provided by libbaltcalc, that uses python integers to perform fast,
seamless, arithmetic on balanced ternary integers, +0- and n0p conversions,
comparisons and other operations. 

Each btint instance contains a `.intval`
attribute which contains one python integer. For performance reasons, some
sections of SBTCVM Gen2-9's codebase works with, and changes, this attribute
directly. namely the CPU.