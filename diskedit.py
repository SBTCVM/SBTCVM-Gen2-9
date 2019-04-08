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

validenttypes=["trom"]

def from_diskmap(diskmap):
	diskmapfile=open(diskmap, "r")
	diskpath=(diskmap.rsplit('.', 1)[0])+".tdsk1"
	print("Checking to see if all files exist...")
	lineno=0
	for ent in diskmapfile:
		ent=ent.replace("\n", "")
		ent=ent.rsplit("#", 1)[0]
		lineno+=1
		if lineno==1:
			label=ent
		elif ent!="":
			try:
				enttype, entsource, entdest = ent.split(";")
			except ValueError:
				sys.exit("Malformed entry in diskmap: \n '" + ent + "'")
			if enttype not in validenttypes:
				sys.exit("Invalid entry type feild value: \n '" + enttype + "'")
			sourcereturn=iofuncts.findtrom(entsource, exitonfail=1, exitmsg="ERROR: Entry Source file: '" + entsource + "' Not found.", dirauto=1)
			if sourcereturn==None:
				sys.exit("Source Entry does not exist, is misspelled, or has the wrong path: \n '" + entsource + "'")
	diskmapfile.seek(0)
	diskdict={}
	lineno=0
	print("Done. Constructing Disk file dictionary...")
	for ent in diskmapfile:
		ent=ent.replace("\n", "")
		ent=ent.rsplit("#", 1)[0]
		lineno+=1
		if lineno==1:
			label=ent
		elif ent!="":
			enttype, entsource, entdest = ent.split(";")
			###trom enttype's get their data stored away verbatim.
			if enttype=="trom":
				filelist=[]
				sourcefile=iofuncts.loadtrom(entsource, exitonfail=1, exitmsg="ERROR: Entry Source file: '" + entsource + "' Not found.", dirauto=1)
				for line in sourcefile:
					i,o=line.replace("\n", "").split(",")
					filelist.append([btint(int(i)), btint(int(o))])
				diskdict[entdest]=filelist
				sourcefile.close()
	print("Saving disk...")
	diskclass=td1.disk(label, diskdict, diskpath)
	diskmapfile.close()
	td1.savedisk(diskclass)
	print(diskpath)



if __name__=="__main__":
	try:
		cmd=sys.argv[1]
	except IndexError:
		cmd=None
	try:
		arg=sys.argv[2]
	except IndexError:
		arg=None
	if cmd in ["-h", "--help"]:
		print('''SBTVDI Disk Image Edit Utility v1.0''')
		print('''Help:
	--new [*.diskmap] - Build a new disk from a diskmap file. ''')
	if cmd=="--new":
		if arg==None:
			sys.exit("Please specify a diskmap to construct disk image with.")
		diskmappath=iofuncts.findtrom(arg, ext=".diskmap", exitonfail=1, exitmsg="diskmap file was not found.", dirauto=1)
		print("Found diskmap: '" + diskmappath + "'")
		from_diskmap(diskmappath)
	#todo: --update: replace files specified in diskmap
	#todo: file import/export, text file support for diskmap files.