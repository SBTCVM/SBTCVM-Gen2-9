#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
from . import iofuncts
from . import libtextcon as tcon

import os
import sys

class disk:
	def __init__(self, label, files, filename, readonly=0, ramdisk=0):
		self.files=files
		self.label=label
	def fload_ascii(self, filename):
		if filename in self.files:
			return self.files[filename]
		else:
			return 1



def loaddisk(filename, readonly=0):
	diskfile=iofuncts.loadtrom(filename, ext=".tdsk1", exitonfail=0, dirauto=1)
	if diskfile==None:
		return "Unable to find tdsk1 image!"
	try:
		diskdat=diskfile.read()
		diskdat=diskdat.split("{")
		headdat=diskdat[0].split("\n")
		label=headdat[0]
		filecount=int(headdat[1])
		if filecount>len(diskdat)-1:
			return "Disk reports a file count '" + str(filecount) + "' that is higher than actual number of files '" + str(len(diskdat)-1) + "'"

		if filecount<len(diskdat)-1:
			return "Disk reports a file count '" + str(filecount) + "' that is lower than actual number of files '" + str(len(diskdat)-1) + "'"
		
		filedict={}
		
		for diskfile in diskdat[1:]:
			linecount=0
			filelist=[]
			for line in diskfile.split("\n"):
				if linecount==0:
					filename=line
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
			filedict[filename]=filelist
	except ValueError:
		return "Bad disk header information"
	except IndexError:
		return "Corrupt Disk file table! unable to load!"
	return disk(label, filedict, filename, readonly=readonly)

diskret=loaddisk("disktest+test.tdsk1", 0)
if isinstance(diskret, str):
	print(diskret)
else:
	print(diskret.label)
	for dfile in diskret.files:
		print("File: " + dfile + " Nonets: " + str(len(diskret.files[dfile])*2))