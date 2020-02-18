#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
from . import iofuncts
from . import libtextcon as tcon

import os
import sys

#limitation constants:
fsizemax=19683
fcountmax=243


class disk:
	def __init__(self, label, files, filename=None, readonly=0, ramdisk=0):
		self.files=files
		self.label=label
		self.fname=filename
		self.ro=readonly
		self.rd=ramdisk
	def fload_ascii(self, filename):
		if filename in self.files:
			return self.files[filename]
		else:
			return 1

def ramdisk():
	return disk("SBTVDI Ramdisk", {}, ramdisk=1)


def loaddisk(filename, readonly=0):
	tdskname=iofuncts.findtrom(filename, ext=".tdsk1", exitonfail=0, dirauto=1)
	if tdskname==None:
		return "Unable to find tdsk1 image!"
	tdskobj=open(tdskname, "r")
	try:
		diskdat=tdskobj.read()
		tdskobj.close()
		diskdat=diskdat.split("{")
		headdat=diskdat[0].split("\n")
		label=headdat[0]
		filecount=int(headdat[1])
		if filecount>len(diskdat)-1:
			return "Disk reports a file count '" + str(filecount) + "' that is higher than actual number of files '" + str(len(diskdat)-1) + "'"

		if filecount<len(diskdat)-1:
			return "Disk reports a file count '" + str(filecount) + "' that is lower than actual number of files '" + str(len(diskdat)-1) + "'"
		
		if len(diskdat)-1>fcountmax:
			return "Disk contains more than 243 files: '" + str(len(diskdat)-1) + "'"
		filedict={}
		
		for diskfile in diskdat[1:]:
			linecount=0
			filelist=[]
			
			for line in diskfile.split("\n"):
				if linecount==0:
					dfile=line
					if len(diskfile.split("\n"))>fsizemax:
						return "File '" + dfile + "': Is beyond 39366 Nonets! '" + str(len(diskfile.split("\n"))*2) + "'"
				elif line=="":
					pass
				else:
					try:
						i,o=line.replace("\n", "").split(",")
						filelist.append([btint(int(i)), btint(int(o))])
						#print(filelist)
					except ValueError as err:
						#print(line)
						#print(err)
						return "Corrupt file data sequence V!"
						
					except IndexError as err:
						#print(err)
						return "Corrupt file data sequence!"
						
				linecount+=1
			filedict[dfile]=filelist
	except ValueError:
		return "Bad disk header information"
	except IndexError:
		return "Corrupt Disk file table! unable to load!"
	return disk(label, filedict, tdskname, readonly=readonly)

#saves disk object contents to its origin *.tdsk1 image.
def savedisk(diskobj):
	#sanity checks
	if diskobj.ro:
		raise ValueError("Disk Object is set read only!")
	if diskobj.rd:
		raise ValueError("Disk Object is a ramdisk. It contains no filename to save to.")
	if diskobj.fname==None:
		raise ValueError("Disk Object has 'None' for the filename. This is ONLY permitted for ramdisks!")
	#build tdsk1 datastructure
	outstr=diskobj.label + "\n" + str(len(diskobj.files)) + "\n"
	for dfile in diskobj.files:
		outstr=outstr+"{"+dfile+"\n"
		for fdat in diskobj.files[dfile]:
			outstr=outstr+str(int(fdat[0]))+","+str(int(fdat[1]))+"\n"
	#save tdsk1 file.
	diskfile=open(diskobj.fname, "w")
	diskfile.write(outstr)
	diskfile.close()

##basic disk load/file read/save test code
#diskret=loaddisk("disktest+test.tdsk1", 0)
#if isinstance(diskret, str):
	#print(diskret)
#else:
	#print(diskret.label)
	#for dfile in diskret.files:
		#print("File: " + dfile + " Nonets: " + str(len(diskret.files[dfile])*2))
	#savedisk(diskret)