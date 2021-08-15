# List of dependencies of Bench:

Special Note: Bench's .vmconf setup depends on `dos` being a valid disk,
as its loaded into drive 1 so dos.app functions correctly.

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
version number constants, mouse cursor and framelock code.

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

#### sndkern_lib
Holds command constants and macros used by Bench apps and sndkern.tri to communicate
over the cross.io lanes, between the main CPU and CoCPU.

#### bench_lib
Contains various technical macros for running `.app`s and returning to the desktop.
