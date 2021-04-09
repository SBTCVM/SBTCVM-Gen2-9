# List of dependencies of Bench:

## Standard Library

#### doslib
used by dos.app for initializing command.txe

#### plrle_noalpha
used heavily by Bench for backgrounds, icons, etc.

#### segment
used to display text in various apps.



## Internal Bench Libraries
(these are found in the 'lib' directory of bench's source)

#### common
startup tune, version number constants, mouse cursor and framelock code.

 - has no dependencies.

#### ui
contains the 'taskbar' drawing code.

 - depends on segment
 - depends on plrle_noalpha

#### yn_dialog
Presents a yes/no dialog to the user, with a customized message.

 - depends on commom (internal)
 - depends on segment
 - depends on plrle_noalpha

## Other
#### dos.app
dos.app will attempt to load the SBTCVM-DOS TDSK1 image via SBTVDI commands.