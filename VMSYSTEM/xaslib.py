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
