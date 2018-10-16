#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
from . import libtextcon as tcon
from . import g2asmlib
btint=libbaltcalc.btint
import os
import sys
from subprocess import call
tritvalid="+0-pn"
#SBTCVM assembly v3 main routine library.

xascmds=[]

xasvers='v1.0.1'
versint=(1, 0, 1)

shellwelcome="---SBTCVM XAS shell " + xasvers + ". Ready.---"

class xascmd:
	def __init__(self, xcmd, execstr, ispython, takesfile):
		self.takesfile=takesfile
		self.xcmd=xcmd
		self.execstr=execstr
		self.ispython=ispython
print("loading xas plugins...")

plugpath=os.path.join(".", "plugins")
for plugin in os.listdir(plugpath):
	if plugin.lower().endswith(".xascmd"):
		plugfile=open(os.path.join(plugpath, plugin), 'r')
		for line in plugfile:
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
			if ';' in line:
				try:
					xcmd, execstr, ispython, takesfile = line.split(';')
					xascmds.extend([xascmd(xcmd, execstr, ispython, takesfile)])
				except IndexError:
					continue
print("plugins loaded.")


verinfo="SBTCVM XAS Shell " + xasvers + "\nPart Of SBTCVM Gen 2-9"


helptext='''----XAS shell help:----
--common--
   help: this text.
   exit: exit shell.
   print [arg]: print text
   list/ls/dir [path]: list a path. i.e. 'ls APPS+gtt' would list APPS/gtt
      Also accepts / and \ as path delineators. only shows files with
      relevant XAS commands. paths are CASE SENSITIVE.
   find [string]: Search filenames containing [string]. only shows files with
      relevant XAS commands.
--build--
   xas: run xas script
   asm [tasm source file]: SBTCVM assembler
   stnp [stnp source file]: SBTCVM Simplified Ternary Numeric Programming
      Language (SSTNPL)
--VM--
   runc [trom image]: run the VM with curses frontend. 
      [BROKEN PLEASE RUN VM DIRECTLY via SBTCVM_G2_9.py]
--tools--
   trominfo [trom image]: get some basic info on a trom. i.e. size.
   dump [trom image]: Dump TROM image
   dumpnp [trom image]: Dump TROM image in n0p format (romdump.py -dnp)
   vdump [trom image]: Dump TROM image in verbose format (romdump.py -r)
   vdumpnp [trom image]: Dump TROM image in verbose n0p format
      (romdump.py -rnp)
'''


abouttext='''SBTCVM eXtensible Assembly Script (XAS) v1
interactive shell mode.
''' + xasvers + '''
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
  
  '''
#generic fileinfo printer (used by find and list)
def fileinfo(filen, pathx):
	if filen.lower().endswith(".trom"):
		print("Rom Image  : " + pathx)
	elif filen.lower().endswith(".tasm"):
		print("Assembly   : " + pathx)
	elif filen.lower().endswith(".stnp"):
		print("SSTNPL     : " + pathx)
	elif filen.lower().endswith(".xas"):
		print("XAS script : " + pathx)
	elif filen.lower().endswith(".nsp"):
		print("NSP library: " + pathx)

#shell input function
def getinput():
	try:
		try:
			return raw_input('>')
		except NameError:
			return input('>')
	except KeyboardInterrupt:
		print("Keyboard Interrupt. Exiting.")
		return 'exit'

#shell input function
def getsubinput(prompt=">"):
	try:
		try:
			return raw_input(prompt)
		except NameError:
			return input(prompt)
	except KeyboardInterrupt:
		print("\nPlease press Ctrl+C again to exit.")
		return ""

#Print function for findcmd
def matcherprint(filen, search, pathx, dirshow=0):
	if dirshow:
		if search.lower() in filen.lower():
			print("Directory  : " + pathx)
	else:
		if search.lower() in filen.lower():
			fileinfo(filen, pathx)

#find: filename search command.
def findcmd(search):
	if search==None:
		print("XAS ERROR: No search string given!")
		return
	print("Search Results For: '" + search + "':")
	for smartd in iofuncts.smartpaths:
		for filen in os.listdir(smartd):
			joinedpath=os.path.join(smartd, filen)
			if os.path.isdir(joinedpath):
				if filen.startswith("r_"):
					for filesub in os.listdir(joinedpath):
						matcherprint(filesub, search, smartd + "+" + filen + "+" + filesub)
				matcherprint(filen, search, smartd + "+" + filen, dirshow=1)
			elif os.path.isfile(joinedpath):
				matcherprint(filen, search, smartd + "+" + filen)
			
		

#directory listing helper for listcmd
def showlisting(realpath, pathdesc):
	print("------listing of: '" + pathdesc + "'")
	for filen in sorted(os.listdir(realpath)):
		if os.path.isfile(os.path.join(realpath, filen)):
			fileinfo(filen, filen)
			#else:
			#	print("Other      : " + filen)
		elif os.path.isdir(os.path.join(realpath, filen)):
			if not filen.startswith("."):
				print("Directory  : " + filen)
#list: directory listing command.
def listcmd(path):
	if path==None or path.startswith("."):
		path="."
	path=path.replace("/", "+").replace("\\", "+").replace("..", "").replace(":\\", "")
	pathlist=path.split("+")
	pathdesc=path
	if len(pathlist)==0:
		realpath="."
	else:
		if pathlist[0]=="0":
			pathlist[0]=os.path.join("disk", "0")
			pathdesc="Drive 0"
		if pathlist[0]=="1":
			pathlist[0]=os.path.join("disk", "1")
			pathdesc="Drive 1"
		realpath=os.path.join(*pathlist)
	if os.path.isdir(realpath):
		showlisting(realpath, pathdesc)
		return
	else:
		print("searching for directory...")
		for smartd in iofuncts.smartpaths:
			if os.path.isdir(os.path.join(smartd, realpath)):
				showlisting(os.path.join(smartd, realpath), smartd.replace("\\", "+").replace("/", "+") + "+" + pathdesc)
				return
	print("XAS ERROR: path not found.")
		

#interactive interpreter
def xasshell():
	print(shellwelcome)
	try:
		import readline
	except ImportError:
		print("failed to load readline.")
	lineno=1
	while True:
		line=getinput()
		lineno+=1
		if line.endswith("\n"):
			line=line[:-1]
		if ';' in line:
			cmd, arg = line.split(';', 1)
		elif ' ' in line:
			cmd, arg = line.split(' ', 1)
		else:
			cmd=line
			arg=None
		if cmd=="xas":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".xas", exitonfail=0, exitmsg="XAS ERROR: xas script: '" + arg + "' was not found. Line: '" + str(lineno) + "'", dirauto=1)
				if pathx==None:
					print("XAS ERROR: xas script '" + arg + "' not found!")
				else:
					print("----XAS script: '" + arg + "'")
					if xasparse(pathx, 0, "  "):
						print("-The script was not run successfully.\n")
					else:
						print("-Subscript Done.\n")
					print(shellwelcome)
			else:
				print("XAS ERROR: no argument after command: xas. Line: '" + str(lineno) + "'")	
		elif cmd=="asm":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".tasm", exitonfail=0, exitmsg="XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "'", dirauto=1)
				if pathx==None:
					print("XAS ERROR: Assembly source file '" + arg + "' not found!")
				else:
					print("assemble: '" + arg + "'")
					
					if g2asmlib.assemble(pathx, 0, "  ", exitonerr=0):
						print("Assembler returned an error.\n")
					else:
						print("Done.\n")
					print(shellwelcome)
			else:
				print("XAS ERROR: no argument after command: asm. Line: '" + str(lineno) + "'")
		elif cmd=="print":
			print(arg)
		elif cmd=="help":
			print(helptext)
		elif cmd=="about":
			print(abouttext)
		elif cmd in ["ver", "version", "info"]:
			print(verinfo)
		elif cmd=="exit":
			return
		elif cmd in ["list", "ls", "dir"]:
			listcmd(arg)
		elif cmd in ["find"]:
			findcmd(arg)
		if cmdvalid(cmd):
			for cmdobj in xascmds:
				if cmd==cmdobj.xcmd:
					if cmdobj.ispython:
						if cmdobj.takesfile and arg!=None:
							print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "' file argument: '" + arg + "'")
							try:
								if call(['python']+cmdobj.execstr.split(" ")+[arg])!=0:
									print("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "'")
							except KeyboardInterrupt:
								pass
							print(shellwelcome)
						else:
							print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "'")
							try:
								if call(['python']+cmdobj.execstr.split(" "))!=0:
									print("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "'")
							except KeyboardInterrupt:
								pass
							print(shellwelcome)
	print(ppx + "xas finished. exiting...")

def cmdvalid(cmd):
	if cmd=="runc":
		print('''!!!!!!! WARNING !!!!!!!
runc currently has a bug where terminal sessions are
broken after terminating the vm with Ctrl+C
PLEASE RUN SBTCVM_G2_9.py DIRECTLY!!!!!!! Press enter to return to prompt.
If your testing this, please enter 'yes' then press enter.''')
		if getsubinput("Are you sure?>")=="yes":
			return 1
		else:
			return 0
	return 1
	

#script interpreter 
def xasparse(scrpath, syntaxonly=0, printprefix=""):
	ppx=printprefix
	xasfile=open(scrpath, 'r')
	print(ppx + "SBTCVM Assembly Script (XAS) v1")
	print(ppx + "running: '" + scrpath + "'\n")
	lineno=1
	for line in xasfile:
		lineno+=1
		if line.endswith("\n"):
			line=line[:-1]
		if '#' in line:
			line=line.rsplit("#", 1)[0]
		if ';' in line:
			cmd, arg = line.split(';', 1)
		elif ' ' in line:
			cmd, arg = line.split(' ', 1)
		else:
			cmd=line
			arg=None
		if cmd=="xas":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".xas", exitonfail=0, exitmsg="XAS ERROR: xas script: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'", dirauto=1)
				if pathx==None:
					print("XAS ERROR: xas script: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
					return 1
				if pathx!=scrpath:
					print(ppx + "----XAS subscript: '" + arg + "'")
					if xasparse(pathx, syntaxonly, printprefix+"  "):
						return 1
					print(ppx + "-Subscript Done.\n")
				else:
					print(ppx + "XAS ERROR: Subscript loop error. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
					return 1
			else:
				print(ppx + "XAS ERROR: no argument after command: xas. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
				return 1
		elif cmd=="asm":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".tasm", exitonfail=0, exitmsg="XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'", dirauto=1)
				
				if pathx==None:
					print("XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
					return 1
				print(ppx + "assemble: '" + arg + "'")
				if g2asmlib.assemble(pathx, syntaxonly, printprefix+"  ", exitonerr=0):
					print(ppx + "ERROR.")
					return 1
				print(ppx + "Done.\n")
			else:
				print(ppx + "XAS ERROR: no argument after command: asm. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
				return 1
		elif cmd=="print":
			if arg!=None:
				print(ppx + "--SCRIPT: " + arg)
		elif cmd=="exit":
			break
		for cmdobj in xascmds:
			if cmd==cmdobj.xcmd:
				if cmdobj.ispython:
					if cmdobj.takesfile and arg!=None:
						print(ppx + "plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "' file argument: '" + arg + "'")
						if call(['python']+cmdobj.execstr.split(" ")+[arg])!=0:
							print(ppx + "XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "' in: '" + scrpath + "'")
							return 1
						print(ppx + "Done.\n")
					else:
						print(ppx + "plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "'")
						if call(['python']+cmdobj.execstr.split(" "))!=0:
							print(ppx + "XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "' in: '" + scrpath + "'")
							return 1
						print(ppx + "Done.\n")
	print(ppx + "xas finished. exiting...")
	xasfile.close()
	return 0
