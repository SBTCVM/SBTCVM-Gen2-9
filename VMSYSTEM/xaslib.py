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

xasvers='v1.0.0'
versint=(1, 0, 0)
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


helptext='''----XAS shell help:----
--common--
help: this text.
exit: exit shell.
print [arg]: print text
--build--
xas: run xas script
asm [tasm source file]: SBTCVM assembler
stnp [stnp source file]: SBTCVM Simplified Ternary Numeric Programming
       Language (SSTNPL)
--VM--
runc [trom image]: run the VM with curses frontend.
--tools--
dump [trom image]: Dump TROM image
dumpnp [trom image]: Dump TROM image in n0p format (same as romdump.py -dnp)
vdump [trom image]: Dump TROM image in verbose format (same as romdump.py -r)
vdumpnp [trom image]: Dump TROM image in verbose n0p format
       (same as romdump.py -rnp)
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

def getinput():
	try:
		try:
			return raw_input('>')
		except NameError:
			return input('>')
	except KeyboardInterrupt:
		print("Keyboard Interrupt. Exiting.")
		return 'exit'


def xasshell():
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
				pathx=iofuncts.findtrom(arg, ext=".xas", exitonfail=0, exitmsg="XAS ERROR: xas script: '" + arg + "' was not found. Line: '" + str(lineno) + "'")
				if pathx==None:
					print("XAS ERROR: xas script '" + arg + "' not found!")
				elif pathx!=scrpath:
					print("----XAS script: '" + arg + "'")
					xasparse(pathx, syntaxonly, "  ")
					print("-Subscript Done.\n")
				else:
					print("XAS ERROR: Subscript loop error. Line: '" + str(lineno) + "'")	
			else:
				print("XAS ERROR: no argument after command: xas. Line: '" + str(lineno) + "'")	
		elif cmd=="asm":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".tasm", exitonfail=0, exitmsg="XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "'")
				if pathx==None:
					print("XAS ERROR: Assembly source file '" + arg + "' not found!")
				else:
					print("assemble: '" + arg + "'")
					g2asmlib.assemble(pathx, syntaxonly, printprefix+"  ")
					print("Done.\n")
			else:
				print("XAS ERROR: no argument after command: asm. Line: '" + str(lineno) + "'")
		elif cmd=="print":
			print(arg)
		elif cmd=="help":
			print(helptext)
		elif cmd=="about":
			print(abouttext)
		elif cmd=="exit":
			return
		for cmdobj in xascmds:
			if cmd==cmdobj.xcmd:
				if cmdobj.ispython:
					if cmdobj.takesfile and arg!=None:
						print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "' file argument: '" + arg + "'")
						if call(['python']+cmdobj.execstr.split(" ")+[arg])!=0:
							print("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "'")
						print("Done.\n")
					else:
						print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "'")
						if call(['python']+cmdobj.execstr.split(" "))!=0:
							print("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "'")
						print("Done.\n")
	print(ppx + "xas finished. exiting...")


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
				pathx=iofuncts.findtrom(arg, ext=".xas", exitonfail=1, exitmsg="XAS ERROR: xas script: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
				if pathx!=scrpath:
					print(ppx + "----XAS subscript: '" + arg + "'")
					xasparse(pathx, syntaxonly, printprefix+"  ")
					print(ppx + "-Subscript Done.\n")
				else:
					sys.exit(ppx + "XAS ERROR: Subscript loop error. Line: '" + str(lineno) + "' in: '" + scrpath + "'")	
			else:
				sys.exit(ppx + "XAS ERROR: no argument after command: xas. Line: '" + str(lineno) + "' in: '" + scrpath + "'")	
		elif cmd=="asm":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".tasm", exitonfail=1, exitmsg="XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
				print(ppx + "assemble: '" + arg + "'")
				g2asmlib.assemble(pathx, syntaxonly, printprefix+"  ")
				print(ppx + "Done.\n")
			else:
				sys.exit(ppx + "XAS ERROR: no argument after command: asm. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
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
							sys.exit(ppx + "XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "' in: '" + scrpath + "'")
						print(ppx + "Done.\n")
					else:
						print(ppx + "plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "'")
						if call(['python']+cmdobj.execstr.split(" "))!=0:
							sys.exit(ppx + "XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "' in: '" + scrpath + "'")
						print(ppx + "Done.\n")
	print(ppx + "xas finished. exiting...")
	xasfile.close()
