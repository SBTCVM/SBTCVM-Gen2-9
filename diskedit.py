#!/usr/bin/env python
import os
if not os.path.isdir("vmsystem"):
    print("changing to script location...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
import vmsystem.tdisk1lib as td1
import sys
import vmsystem.iofuncts as iofuncts
import vmsystem.libbaltcalc as libbaltcalc
from vmsystem.libbaltcalc import btint

validenttypes = ["trom"]


def trom_to_diskfilelist(fileobj, filename):
    try:
        filelist = []
        for line in fileobj:
            i, o = line.replace("\n", "").split(",")
            filelist.append([btint(int(i)), btint(int(o))])
    except IndexError:
        sys.exit("ERROR: corrupt TROM image file! (" + filename + ")")
    return filelist


def append_file(diskfile, file_to_append, filetype, targetname):
    disk = td1.loaddisk(diskfile)
    if isinstance(disk, str):
        sys.exit("TDSK1 image '" + diskfile + "' not found...")
    if filetype not in validenttypes:
        sys.exit("invalid file type value: '" + filetype + "'")
    if filetype == "trom":
        sourcefile = iofuncts.loadtrom(
            file_to_append,
            exitonfail=1,
            exitmsg="ERROR: Source file: '" +
            file_to_append +
            "' Not found.",
            dirauto=1)
        filelist = trom_to_diskfilelist(sourcefile, file_to_append)
        disk.files[targetname] = filelist
        td1.savedisk(disk)


def from_diskmap(diskmap, disk_append=False):
    diskmapfile = open(diskmap, "r")
    diskpath = (diskmap.rsplit('.', 1)[0]) + ".tdsk1"
    print("Checking to see if all files exist...")
    lineno = 0
    for ent in diskmapfile:
        ent = ent.replace("\n", "")
        ent = ent.rsplit("#", 1)[0]
        lineno += 1
        if lineno == 1:
            label = ent
        elif ent != "":
            try:
                enttype, entsource, entdest = ent.split(";")
            except ValueError:
                sys.exit("Malformed entry in diskmap: \n '" + ent + "'")
            if enttype not in validenttypes:
                sys.exit(
                    "Invalid entry type feild value: \n '" +
                    enttype +
                    "'")
            sourcereturn = iofuncts.findtrom(
                entsource,
                exitonfail=1,
                exitmsg="ERROR: Entry Source file: '" +
                entsource +
                "' Not found.",
                dirauto=1)
            if sourcereturn is None:
                sys.exit(
                    "Source Entry does not exist, is misspelled, or has the wrong path: \n '" +
                    entsource +
                    "'")
    diskmapfile.seek(0)
    if not disk_append:
        diskdict = {}
        print("Done. Constructing Disk file dictionary...")
    else:
        diskclass = td1.loaddisk(opt)
        if isinstance(diskclass, str):
            sys.exit("TDSK1 image: '" + opt + "' not found.")
        diskdict = diskclass.files
        print("Done. Appending to Disk file dictionary...")
    lineno = 0

    for ent in diskmapfile:
        ent = ent.replace("\n", "")
        ent = ent.rsplit("#", 1)[0]
        lineno += 1
        if lineno == 1:
            label = ent
        elif ent != "":
            enttype, entsource, entdest = ent.split(";")
            # trom enttype's get their data stored away verbatim.
            if enttype == "trom":
                filelist = []
                sourcefile = iofuncts.loadtrom(
                    entsource,
                    exitonfail=1,
                    exitmsg="ERROR: Entry Source file: '" +
                    entsource +
                    "' Not found.",
                    dirauto=1)
                # for line in sourcefile:
                # i,o=line.replace("\n", "").split(",")
                # filelist.append([btint(int(i)), btint(int(o))])
                filelist = trom_to_diskfilelist(sourcefile, entsource)
                diskdict[entdest] = filelist
                sourcefile.close()
    print("Saving disk...")
    if not disk_append:
        diskclass = td1.disk(label, diskdict, diskpath)
    diskmapfile.close()
    td1.savedisk(diskclass)
    print(diskpath)


if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
    except IndexError:
        cmd = None
    try:
        arg = sys.argv[2]
    except IndexError:
        arg = None
    try:
        opt = sys.argv[3]
    except IndexError:
        opt = None
    try:
        opt2 = sys.argv[4]
    except IndexError:
        opt2 = None
    try:
        opt3 = sys.argv[5]
    except IndexError:
        opt3 = None
    if cmd in ["-h", "--help"]:
        print('''SBTVDI Disk Image Edit Utility v1.0''')
        print('''Help:
	--new [*.diskmap] - Build a new disk from a diskmap file.
	--append [*.diskmap] [*.tdsk1] - append/update files in an EXISTING disk from a diskmap file.
	--appendfile [*.tdsk1] [sourcefile] [targetname] [type] - append/update a single file in an EXISTING disk.''')
    elif cmd == "--new":
        if arg is None:
            sys.exit("Please specify a diskmap to construct disk image with.")
        diskmappath = iofuncts.findtrom(
            arg,
            ext=".diskmap",
            exitonfail=1,
            exitmsg="diskmap file was not found.",
            dirauto=1)
        print("Found diskmap: '" + diskmappath + "'")
        from_diskmap(diskmappath)
    elif cmd == "--append":
        if arg is None or opt is None:
            sys.exit(
                "Please specify '--append [*.diskmap] [existing *.tdsk1]'")
        diskmappath = iofuncts.findtrom(
            arg,
            ext=".diskmap",
            exitonfail=1,
            exitmsg="diskmap file was not found.",
            dirauto=1)
        print("Found diskmap: '" + diskmappath + "'")
        from_diskmap(diskmappath, disk_append=opt)
    elif cmd == "--appendfile":
        if arg is None or opt is None or opt2 is None or opt3 is None:
            sys.exit(
                "please specify '--appendfile [*.tdsk1] [sourcefile] [targetname] [type]'")
        append_file(arg, opt, opt3, opt2)
    elif cmd is None:
        print("try diskedit.py -h for help.")
    elif cmd.startswith("-"):
        print("Unknown option: '" + cmd + "' try diskedit.py -h for help.")
    # todo: file import/export, text file support for diskmap files.
