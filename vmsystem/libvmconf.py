#!/usr/bin/env python
from . import iofuncts


def check_has_vmconf(filename):
    vmconf = iofuncts.findtrom(
        filename,
        ext=".vmconf",
        exitonfail=0,
        dirauto=1)
    if vmconf is not None:
        return True
    return False


default_cfg = {"rom0": "VDIBOOT",
               "rom1": None,
               "vdi0": None,
               "vdi1": None,
               "name": None,
               "cocpu_halt": True}

bool_names = ["cocpu_halt"]
int_names = []


def load_vmconf(filename):
    filename = iofuncts.findtrom(
        filename,
        ext=".vmconf",
        exitonfail=0,
        dirauto=1)
    dispname = "VMCONF ( " + filename + " ): "
    return iofuncts.cfg_load(
        filename,
        default_cfg,
        bool_names,
        int_names,
        dispname,
        use_raw_filename=True)
