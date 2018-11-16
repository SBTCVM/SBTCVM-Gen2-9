#!/usr/bin/env python
import os
if not os.path.isdir("vmsystem"):
	print("changing to script location...")
	os.chdir(os.path.dirname(os.path.abspath(__file__)))


import vmsystem.libbaltcalc as libbaltcalc
from vmsystem.libbaltcalc import btint
import vmsystem.libtextcon as tcon
import time
import sys
import vmsystem.iofuncts as iofuncts
import vmsystem.g2common as g2com

vers=sys.version_info[0]

#just point xrange to range in python3.
if vers==3:
	xrange=range

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
			line=line.replace("\n", "")
			ival0, ival1 = line.split(",")
			trval0=btint(int(ival0))
			trval1=btint(int(ival1))
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
			line=line.replace("\n", "")
			ival0, ival1 = line.split(",")
			trval0=btint(int(ival0))
			trval1=btint(int(ival1))
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
		fileobj.seek(0)
		mempos=-9842
		isstring=0
		for line in fileobj:
			mempos+=1
			if mempos in xrange(start, end+1):
				line=line.replace("\n", "")
				ival0, ival1 = line.split(",")
				if searchpass==0:
					trval=btint(int(ival1))
				else:
					trval=btint(int(ival0))
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
	

def romdump_stringfind_interlaced(fileobj, start, end):
	
	if start==None:
		start=-9841
	if end==None:
		end=9841
	if end<start:
		sys.exit("Error range start must be less than end")
	pstring=""
	fileobj.seek(0)
	mempos=-9842
	isstring=0
	stringcnt=0
	for line in fileobj:
		mempos+=1
		if mempos in xrange(start, end+1):
			line=line.replace("\n", "")
			ival0, ival1 = line.split(",")
			for trval in [btint(int(ival1)), btint(int(ival0))]:
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
			line=line.replace("\n", "")
			ival0, ival1 = line.split(",")
			trval0=btint(int(ival0))
			trval1=btint(int(ival1))
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
			pstring += " | adr:" + str(mempos).rjust(6)
			print(pstring)

def rominfo(tromfile):
	print("path: " + tromfile)
	tromobj=open(tromfile)
	g2com.standardsizeprint(g2com.gettromsize(tromobj))


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
	if cmd not in ["-d", "-dnp", "-r", "-rnp", "-i", "--info", "-t1", "-t2", "-t0", "-t", "-f", "-f2"]:
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
		print('''SBTCVM Gen2 romdump utility. v1.1.0
   -h --help: this help
   -v --version: version
   -a, --about: about SBTCVM
   -i [trom]: show general information on trom. including size.
   -f [trom]: search for strings and print them per-line with their starting
      addresses.
   -f2 [trom]: same as -f, but try to find interlaced strings instead of normal
      ones.
   -d [trom]: dump contents of trom to standard output in +0- form.
      instructions and data colums separated by two spaces. "  "
      a third column containing the address in signed decmimal
      is separated via a vertical bar "|"
   -r [trom]: same as -d, but also prints chars & decimal values and labels
      address column
   -dnp [trom]: same as -d, but using n0p representation.
   -rnp [trom]: same as -dnp, but also prints chars & decimal values
   -t0/-t [trom]: dump raw character data from data bank (excluding special
      characters)
   -t1 [trom]: dump raw character data from instruction bank (excluding
      special characters)
   -t2 [trom]: dump raw character data from both banks (interlaced, excluding
      special characters)
   [trom]: (with no options) same as -d
   >>> Specifying a start and end address (in signed decimal, space-separated)
      after the rom name enables ranged mode. In this mode, only the range given
      is used. does NOT apply to: -h, -v, -a, and -i
   >>> -f and -f2 will ignore strings less than 2 characters long.
''')
	elif cmd in ["-v", "--version"]:
		print("SBTCVM Gen2 romdump utility. v1.1.0\n" + "part of SBTCVM-Gen2-9 v2.1.0.alpha")
	elif cmd in ["-a", "--about"]:
		print('''SBTCVM Gen2-9 romdump utility.
v1.1.0
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

Copyright (c) 2016-2018 Thomas Leathers and Contributors 

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
		romdump_rawtext(iofuncts.loadtrom(arg, dirauto=1), start, end, bank=0)
	elif cmd in ["-t1"]:
		romdump_rawtext(iofuncts.loadtrom(arg, dirauto=1), start, end, bank=1)
	elif cmd in ["-t2"]:
		romdump_rawtext(iofuncts.loadtrom(arg, dirauto=1), start, end, bank=2)
	elif cmd in ["-f"]:
		romdump_stringfind(iofuncts.loadtrom(arg, dirauto=1), start, end)
	elif cmd in ["-f2"]:
		romdump_stringfind_interlaced(iofuncts.loadtrom(arg, dirauto=1), start, end)
	elif cmd in ["-d"]:
		romdump(iofuncts.loadtrom(arg, dirauto=1), start, end)
	elif cmd in ["-i", "--info"]:
		rominfo(iofuncts.findtrom(arg, dirauto=1))
	elif cmd in ["-dnp"]:
		romdump(iofuncts.loadtrom(arg, dirauto=1), start, end, n0p=1)
	elif cmd in ["-r"]:
		romdumpver(iofuncts.loadtrom(arg, dirauto=1), start, end)
	elif cmd in ["-rnp"]:
		romdumpver(iofuncts.loadtrom(arg, dirauto=1), start, end, n0p=1)
	elif cmd == None:
		print("Tip: try romdump.py -h for help.")
	else:
		romdump(iofuncts.loadtrom(cmd, dirauto=1), start, end)