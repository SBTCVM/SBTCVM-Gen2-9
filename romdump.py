#!/usr/bin/env python
import os
if not os.path.isdir("vmsystem"):
	print("changing to script location...")
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
import vmsystem.tdisk1lib as td1

import vmsystem.libbaltcalc as libbaltcalc
from vmsystem.libbaltcalc import btint
import vmsystem.libtextcon as tcon
import time
import sys
import vmsystem.iofuncts as iofuncts
import vmsystem.g2common as g2com
import vmsystem.libbal27 as bal27

vers=sys.version_info[0]

#just point xrange to range in python3.
if vers>2:
	xrange=range

def TromLoad(fileobj):
	datalist=[]
	for line in fileobj:
		line=line.replace("\n", "")
		ival0, ival1 = line.split(",")
		trval0=btint(int(ival0))
		trval1=btint(int(ival1))
		datalist.append([trval0, trval1])
	return datalist

def DiskLoader(arg, filearg):
	if "^" in arg:
		filename, diskfile = arg.split("^")
	else:
		sys.exit("Must Specify a file inside the TDSK image for this command!")
	dsk=td1.loaddisk(filename, readonly=1)
	if diskfile in dsk.files:
		return dsk.files[diskfile]
	else:
		sys.exit("Cannot find file '" + diskfile + "' In tdsk1 image: '" + filearg)

def InputFileLoader(arg, dirauto=1):
	if arg==None:
		sys.exit("ERROR: no file specified.")
	filearg=arg.split("^")[0]
	fname=iofuncts.findtrom(filearg, dirauto=dirauto, exitonfail=0)
	if fname!=None and "^" not in arg:
		if fname.lower().endswith(".trom"):
			fobj=open(fname, "r")
			return TromLoad(fobj)
		elif fname.lower().endswith(".tdsk1"):
			sys.exit("please specify file via [diskimage^filename].")
			
	else:
		fname=iofuncts.findtrom(filearg, dirauto=dirauto, exitonfail=0, ext=".tdsk1")
		if fname!=None:
			if fname.lower().endswith(".tdsk1"):
				return DiskLoader(arg, filearg)
	sys.exit("Unable to locate TDSK1/TROM.")


def romdump(fileobj, start, end, n0p=0):
	mempos=-9842
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	for line in fileobj:
		mempos+=1
		if mempos in xrange(start, end+1):
			#line=line.replace("\n", "")
			#ival0, ival1 = line.split(",")
			#trval0=btint(int(ival0))
			#trval1=btint(int(ival1
			trval0, trval1 = line
			pstring=trval0.bttrunk(9) + "  " + trval1.bttrunk(9)
			if n0p==1:
				pstring=pstring.replace("-", "n").replace("+", "p")
			pstring += "|" + str(mempos).rjust(6)
			print(pstring)

def romdump_rawtext(fileobj, start, end, bank=1):
	mempos=-9842
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	pstring=""
	for line in fileobj:
		mempos+=1
		if mempos in xrange(start, end+1):
			
			trval0, trval1 = line
			tr0ischar=0
			tr1ischar=0
			if bank==0 or bank==2:
				for char in tcon.allchars:
					if char.dataval==trval1:
						pstring += (char.bldumpstr)
						tr1ischar=1
						
				if not tr1ischar:
					pstring += "."
			if bank==1 or bank==2:
				for char in tcon.allchars:
					if char.dataval==trval0:
						pstring += (char.bldumpstr)
						tr0ischar=1
				if not tr0ischar:
					pstring += "."
	print(pstring)
			

def romdump_stringfind(fileobj, start, end):
	
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	
	for searchpass in [0, 1]:
		pstring=""
		stringcnt=0
		
		mempos=-9842
		isstring=0
		for line in fileobj:
			mempos+=1
			if mempos in xrange(start, end+1):
				if searchpass==0:
					trval=line[1]
				else:
					trval=line[0]
				trischar=0
				for char in tcon.allchars:
					if char.dataval==trval and trval!=0 and trval!=2:
						#Break string on newline
						if char.dataval==1 and isstring==1:
							isstring=0
							if stringcnt>1:
								print(pstring)
							stringcnt=0
						elif char.dataval==1:
							pass
						else:
							#if at start of string, start with pass no. and starting address.
							if isstring==0:
								isstring=1
								pstring=str(searchpass) + ", At " + str(mempos).rjust(5) + " :"
							pstring += (char.bldumpstr)
							stringcnt+=1
						trischar=1
				#break string on non-character.
				if not trischar:
					if isstring==1:
						isstring=0
						if stringcnt>1:
							print(pstring)
						stringcnt=0
	

def b27_char(fileobj, start, end):
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	pstring=""
	inst=""
	data=""
	inst_char=""
	data_char=""
	mempos=-9842
	widcnt=0
	for line in fileobj:
		mempos+=1
		widcnt+=1
		trval0, trval1 = line
		inst=inst + bal27.inttob27(trval0).rjust(4)
		data=data + bal27.inttob27(trval1).rjust(4)
		tr0ischar=0
		tr1ischar=0
		for char in tcon.allchars:
			if char.dataval==trval0:
				inst_char += (char.bldumpstr)
				tr0ischar=1
				
		if not tr0ischar:
			inst_char += "."
		
		for char in tcon.allchars:
			if char.dataval==trval1:
				data_char += (char.bldumpstr)
				tr1ischar=1
				
		if not tr1ischar:
			data_char += "."
		
		if widcnt == 9:
			if mempos in xrange(start, end+1) or mempos-8 in xrange(start, end+1) or start in xrange(mempos-8, mempos) or end in xrange(mempos-8, mempos):
				print(inst + "|" + inst_char + "||" + data + "|" + data_char + "||" + str(mempos-8).rjust(6) + " TO" + str(mempos).rjust(6))
			inst=""
			data=""
			inst_char=""
			data_char=""
			widcnt=0

def romdump_stringfind_interlaced(fileobj, start, end):
	
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	pstring=""
	
	mempos=-9842
	isstring=0
	stringcnt=0
	for line in fileobj:
		mempos+=1
		if mempos in xrange(start, end+1):
			for trval in line:
				trischar=0
				for char in tcon.allchars:
					if char.dataval==trval and trval!=0 and trval!=2:
						#Break string on newline
						if char.dataval==1 and isstring==1:
							isstring=0
							if stringcnt>1:
								print(pstring)
							stringcnt=0
						elif char.dataval==1:
							pass
						else:
							#if at start of string, start with pass no. and starting address.
							if isstring==0:
								isstring=1
								pstring="At " + str(mempos).rjust(5) + " :"
							pstring += (char.bldumpstr)
							stringcnt+=1
						trischar=1
				#break string on non-character.
				if not trischar:
					if isstring==1:
						isstring=0
						if stringcnt>1:
							print(pstring)
						stringcnt=0
	
#verbose rom dump
def romdumpver(fileobj, start, end, n0p=0):
	mempos=-9842
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	for line in fileobj:
		mempos+=1
		if mempos in xrange(start, end+1):
			trval0, trval1 = line
			pstring=trval0.bttrunk(9) + "  " + trval1.bttrunk(9)
			if n0p==1:
				pstring=pstring.replace("-", "n").replace("+", "p")
			tr0ischar=0
			tr1ischar=0
			for char in tcon.allchars:
				
				if char.dataval==trval0:
					pstring += ("  " + char.bldumpstr)
					tr0ischar=1
			if not tr0ischar:
				pstring += "  ."
			for char in tcon.allchars:
				if char.dataval==trval1:
					pstring += ("  " + char.bldumpstr)
					tr1ischar=1
			
			if not tr1ischar:
				pstring += "  ."
			pstring += str(int(trval0)).rjust(8) + str(int(trval1)).rjust(8)
			pstring += bal27.inttob27(int(trval0)).rjust(6) + bal27.inttob27(int(trval1)).rjust(4)
			pstring += " | adr:" + str(mempos).rjust(6)
			print(pstring)

def rominfo(arg, dirauto=1):
	if arg==None:
		sys.exit("ERROR: no file specified.")
	filearg=arg.split("^")[0]
	fname=iofuncts.findtrom(filearg, dirauto=dirauto, exitonfail=0)
	if fname!=None and "^" not in arg:
		if fname.lower().endswith(".trom"):
			fobj=open(fname, "r")
			print("----FileType: TROM: SBTCVM Ternary ROM.")
			print("path: " + filearg)
			g2com.standardsizeprint(g2com.gettromsize(fobj))
			print("--------")
	fname2=iofuncts.findtrom(filearg, dirauto=dirauto, exitonfail=0, ext=".tdsk1")
	if fname2!=None:
		if "^" in arg:
			diskfilename=arg.split("^")[1]
			dsk=td1.loaddisk(filearg, readonly=1)
			if diskfilename in dsk.files:
				filedat=diskfilename
				if diskfilename.lower().endswith(".txe"):
					print("----VDI FileType: TXE:  Ternary Executable. [RAW G2-9 format]")
				else:
					print("----VDI FileType: (?):  Unknown extention.")
				print("File Size: " + g2com.nonetformatted_smart(len(dsk.files[diskfilename])))
				print("--------")
		else:
			if fname2.lower().endswith(".tdsk1"):
				dsk=td1.loaddisk(filearg, readonly=1)
				print("----FileType: TDSK1: Format 1 SBTVDI disk image.")
				print("path: " + filearg)
				disksize=0
				print("Label: " + dsk.label)
				print("files:")
				
				for filex in dsk.files:
					print("    " + filex.ljust(20) + " " + g2com.nonetformatted_smart(len(dsk.files[filex])))
					disksize+=len(dsk.files[filex])
				print("Disk size (virtual): " + g2com.nonetformatted_smart(disksize))
				print("--------")
	else:
		if fname==None:
			sys.exit("ERROR: Cant find TDSK1/TROM image.")
	
	


if __name__=="__main__":
	try:
		cmd=sys.argv[1]
	except IndexError:
		cmd=None
	try:
		arg=sys.argv[2]
	except IndexError:
		arg=None
	#ensure arg is none when just file and range values are passed.
	if cmd not in ["-d", "-dnp", "-r", "-c", "-rnp", "-i", "--info", "-t1", "-t2", "-t0", "-t", "-f", "-f2"]:
		arg=None
	if cmd in ["-a", "-h", "-v", "-i", "--about", "--help", "--version", "--info"]:
		pass
	elif arg!=None:
		try:
			start=int(sys.argv[3])
			end=int(sys.argv[4])
		except IndexError:
			start=None
			end=None
		except ValueError:
			sys.exit("Error: ranged mode requires 2, space-separated signed decimal addresses.")
	else:
		try:
			start=int(sys.argv[2])
			end=int(sys.argv[3])
		except IndexError:
			start=None
			end=None
		except ValueError:
			sys.exit("Error: ranged mode requires 2, space-separated signed decimal addresses.")
	if cmd in ["-h", "--help"]:
		print('''SBTCVM Gen2 romdump utility. v2.0.0
   note: "diskfile" refers to the syntax: tdsk1file^filename_on_disk. 
        use dump -i tdsk1file for filename listing.
   -h --help: this help
   -v --version: version
   -a, --about: about SBTCVM
   -i [trom/diskfile/tdsk1]: show general information on file. including size.
   -f [trom/diskfile]: search for strings and print them per-line with their starting
      addresses.
   -f2 [trom/diskfile]: same as -f, but try to find interlaced strings instead of normal
      ones.
   -c [trom/diskfile]: a Septemvigesimal + BTT2 character output, similar to
      'cannonical' hex+ascii dumps in binary.
   -d [trom/diskfile]: dump contents of trom to standard output in +0- form.
      instructions and data columns separated by two spaces. "  "
      a third column containing the address in signed decimal
      is separated via a vertical bar "|"
   -r [trom/diskfile]: same as -d, but also prints chars, 
      Septemvigesimal (balanced base 27) values,  & decimal
      values, and labels address column.
   -dnp [trom/diskfile]: same as -d, but using n0p representation.
   -rnp [trom/diskfile]: same as -dnp, but also prints chars & decimal values
   -t0/-t [trom/diskfile]: dump raw character data from data bank (excluding special
      characters)
   -t1 [trom/diskfile]: dump raw character data from instruction bank (excluding
      special characters)
   -t2 [trom/diskfile]: dump raw character data from both banks (interlaced, excluding
      special characters)
   [trom/diskfile]: (with no options) same as -d
   >>> Specifying a start and end address (in signed decimal, space-separated)
      after the trom/diskfle name enables ranged mode. In this mode, only the range given
      is used. does NOT apply to: -h, -v, -a, and -i
   >>> -f and -f2 will ignore strings less than 2 characters long.
''')
	elif cmd in ["-v", "--version"]:
		print("SBTCVM Gen2 romdump utility. v2.0.0\n" + "part of SBTCVM-Gen2-9 v2.1.0.alpha")
	elif cmd in ["-a", "--about"]:
		print('''SBTCVM Gen2-9 romdump utility.
v2.0.0
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

Copyright (c) 2016-2020 Thomas Leathers and Contributors 

see readme.md for more information and licensing of media.

  SBTCVM Gen2-9 is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Gen2-9 is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Gen2-9. If not, see <http://www.gnu.org/licenses/>
  
  ''')
	elif cmd in ["-t", "-t0"]:
		romdump_rawtext(InputFileLoader(arg, dirauto=1), start, end, bank=0)
	elif cmd in ["-t1"]:
		romdump_rawtext(InputFileLoader(arg, dirauto=1), start, end, bank=1)
	elif cmd in ["-t2"]:
		romdump_rawtext(InputFileLoader(arg, dirauto=1), start, end, bank=2)
	elif cmd in ["-f"]:
		romdump_stringfind(InputFileLoader(arg, dirauto=1), start, end)
	elif cmd in ["-f2"]:
		romdump_stringfind_interlaced(InputFileLoader(arg, dirauto=1), start, end)
	elif cmd in ["-d"]:
		romdump(InputFileLoader(arg, dirauto=1), start, end)
	elif cmd in ["-i", "--info"]:
		#rominfo(iofuncts.findtrom(arg, dirauto=1))
		rominfo(arg, dirauto=1)
	elif cmd in ["-dnp"]:
		romdump(InputFileLoader(arg, dirauto=1), start, end, n0p=1)
	elif cmd in ["-r"]:
		romdumpver(InputFileLoader(arg, dirauto=1), start, end)
	elif cmd in ["-c"]:
		b27_char(InputFileLoader(arg, dirauto=1), start, end)
	elif cmd in ["-rnp"]:
		romdumpver(InputFileLoader(arg, dirauto=1), start, end, n0p=1)
	elif cmd == None:
		print("Tip: try romdump.py -h for help.")
	elif cmd.startswith("-"):
		print("Unknown option: '" + cmd + "' try romdump.py -h for help.") 
	else:
		romdump(InputFileLoader(cmd, dirauto=1), start, end)
