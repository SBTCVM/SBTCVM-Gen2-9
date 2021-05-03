# VMCONF files

[help index](index.md)


## overview

`.vmconf` files can be used to specify specific startup parameters for 
SBTCVM software, both disk-based, trom-based, and even both.

It also allows programs to specify separate roms for the SBTGA CoCPU (CPU 1), and the second SBTVDI floppy drive.



## options

#### Main TROM (CPU0 TROM)

This is the same as when you specify a trom as an argument to the VM.

**IMPORTANT NOTE:** This defaults to VDIBOOT, the SBTVDI disk bootup firmware/BIOS.

`rom0=filename`

e.g. `rom0=my_auto_dir/main_cpu.trom`

#### SBTGA CoCPU TROM (CPU1 TROM)

This lets you load a separate rom into the CoCPU's memory. Useful with `cocpu_halt=False`

`rom1=filename`

e.g. `rom1=my_auto_dir/sbtga_cocpu.trom`

#### SBTVDI Floppy Drive 0

This is the same as when you specify a tdsk1 image as an argument to the VM.

`vdi0=disk_image_filename`

e.g. `vdi0=my_auto_dir/mydisk.tdsk1`

#### SBTVDI Floppy Drive 1

This lets you specify a tdsk1 image to load into the second SBTVDI Floppy Drive.

`vdi1=disk_image_filename`

e.g. `vdi1=my_auto_dir/mydisk.tdsk1`

#### name

In some frontends, this lets you control the 'friendly' name of the 
given VM instance. e.g. the Pygame Frontend will show this in the window title.


`name=My Amazing Program`

#### cocpu Halt Flag

This is useful when you specify a trom for the CoCPU, and want it to
begin running at startup when the main CPU starts up.

To have the SBTGA COCPU **running** at startup:

`cocpu_halt=False`

To have the SBTGA COCPU **halted** at startup (default):

`cocpu_halt=True`


