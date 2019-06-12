#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
from . import libtextcon as tcon
btint=libbaltcalc.btint
import os
import sys
#from subprocess import call
from subprocess import Popen

def call(*openargs):
	try:
		sub=Popen(*openargs)
		sub.wait()
	except KeyboardInterrupt:
		callINTwait(sub)
	return sub.returncode
	

def callINTwait(sub):
	try:
		sub.wait()
	except KeyboardInterrupt:
		callINTwait(sub)
tritvalid="+0-pn"
#SBTCVM assembly v3 main routine library.

xascmds=[]
import time
xasvers='v2.0.0'
versint=(2, 0, 0)

shellwelcome="\n---SBTCVM XAS shell " + xasvers + ". Ready.---"

class xascmd:
	def __init__(self, xcmd, execstr, ispython, takesfile):
		self.takesfile=takesfile
		self.xcmd=xcmd
		self.execstr=execstr
		self.ispython=ispython
print("loading xas plugins...")

helpitems={}
helplist=[]
helpshort=[]

plugpath=os.path.join(".", "plugins")
for plugin in sorted(os.listdir(plugpath)):
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
	if plugin.lower().endswith(".xashelp"):
		plugfile=open(os.path.join(plugpath, plugin), 'r')
		plugglob=""
		for line in plugfile:
			plugglob=plugglob+line
		firstline, plugglob=plugglob.split("\n", 1)
		helplist.append(firstline)
		helpshort.append("--" + firstline)
		helpbloc=plugglob.split("{")
		try:
			helpbloc.remove('')
		except ValueError:
			continue
		shhelpch=""
		for helpchunk in helpbloc:
			chsplit=helpchunk.split("\n")
			hkeys=chsplit[0].split(",")
			contents=chsplit[1:]
			contents.remove('')
			if contents==[] or hkeys==[""]:
				print(chsplit)
			for hkey in hkeys:
				helpitems[hkey]=contents
			helplist.append("  " + ",".join(hkeys).ljust(5) + " : " + contents[0])
			if shhelpch=="":
				shhelpch=(shhelpch + ",".join(hkeys))
			else:
				shhelpch=(shhelpch + "," + ",".join(hkeys))
		helpshort.append("    " + shhelpch)
print("plugins loaded.")


verinfo="SBTCVM XAS Shell " + xasvers + "\nPart Of SBTCVM Gen 2-9"




abouttext='''SBTCVM eXtensible Assembly Script (XAS) v2
interactive shell mode.
''' + xasvers + '''
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

Copyright (c) 2016-2019 Thomas Leathers and Contributors 

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
def fileinfo(filen, pathx, sublist=0):
	if sublist:
		prfx="    "
	else:
		prfx=""
	if filen.lower().endswith(".trom"):
		print(prfx + "   SBTCVM Rom Image      : " + pathx)
	elif filen.lower().endswith(".tasm"):
		print(prfx + "   Assembler source file : " + pathx)
	elif filen.lower().endswith(".tas0"):
		print(prfx + "   Assembler tas0 Module : " + pathx)
	elif filen.lower().endswith(".stnp"):
		print(prfx + "   SSTNPL Source code    : " + pathx)
	elif filen.lower().endswith(".stnpmfs"):
		print(prfx + "   SSTNPL Module Manifest: " + pathx)
	elif filen.lower().endswith(".diskmap"):
		print(prfx + "   Diskedit Disk Filelist: " + pathx)
	elif filen.lower().endswith(".tdsk1"):
		print(prfx + "   Ternary Disk Image v1 : " + pathx)
	elif filen.lower().endswith(".xas"):
		print(prfx + "   XAS build script      : " + pathx)
	elif filen.lower().endswith(".nsp"):
		print(prfx + "   Assembler NSP library : " + pathx)

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
def matcherprint(filen, search, pathx, dirshow=0, sublist=0):
	if sublist:
		prfx="    "
	else:
		prfx=""
	if dirshow:
		if search.lower() in filen.lower():
			print(prfx + "   Directory   : " + pathx)
			return 1
	else:
		if search.lower() in filen.lower():
			fileinfo(filen, pathx, sublist=sublist)
			return 1
	return 0

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
				matcherprint(filen, search, filen, dirshow=1)
				if filen.startswith("r_"):
					for filesub in os.listdir(joinedpath):
						matcherprint(filesub, search, filesub)
				else:
					for filesub in os.listdir(joinedpath):
						#Detect SBTCVM smart app directories.
						if filesub.startswith("auto_") and search.lower() in filen.lower():
							fileinfo(filesub, filen, sublist=1)
						else:
							matcherprint(filesub, search,  filen + "+" + filesub)
							
				
			elif os.path.isfile(joinedpath):
				matcherprint(filen, search, filen)
			
		

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
				print("   Directory   : " + filen)
				#Detect SBTCVM smart app directories.
				if pathdesc in iofuncts.smartpaths:
					for filesub in os.listdir(os.path.join(realpath, filen)):
						if filesub.startswith("auto_"):
							fileinfo(filesub, filen, sublist=1)
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
		elif cmd=="print":
			print(arg)
		elif cmd=="help":
			if arg==None:
				for line in helpshort:
					print(line)
			elif arg=="all":
				for command in helplist:
					print(command)
			else:
				if arg in helpitems:
					print(arg + ": " + "\n".join(helpitems[arg]))
				
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
		#.xascmd plugin commands.
		if cmdvalid(cmd):
			for cmdobj in xascmds:
				if cmd==cmdobj.xcmd:
					#TODO: non-python commands.
					if cmdobj.ispython:
						if cmdobj.takesfile and arg!=None:
							print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "' file argument: '" + arg + "'\n")
							try:
								if call(['python']+cmdobj.execstr.split(" ")+arg.split(" "))!=0:
									print("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "'")
							except KeyboardInterrupt:
								pass
							print(shellwelcome)
						else:
							print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "'\n")
							try:
								if call(['python']+cmdobj.execstr.split(" "))!=0:
									print("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "'")
							except KeyboardInterrupt:
								pass
							print(shellwelcome)
	print(ppx + "xas finished. exiting...")

def cmdvalid(cmd):
	#if cmd=="runc":
		#print('''!!!!!!! WARNING !!!!!!!
#runc currently has a bug where terminal sessions are
#broken after terminating the vm with Ctrl+C
#PLEASE RUN cur_sbtcvm.py DIRECTLY!!!!!!! Press enter to return to prompt.
#If your testing this, please enter 'yes' then press enter.''')
		#if getsubinput("Are you sure?>")=="yes":
			#return 1
		#else:
			#return 0
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
		#elif cmd=="asm":
			#if arg!=None:
				#pathx=iofuncts.findtrom(arg, ext=".tasm", exitonfail=0, exitmsg="XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'", dirauto=1)
				
				#if pathx==None:
					#print("XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
					#return 1
				#print(ppx + "assemble: '" + arg + "'")
				#if g2asmlib.assemble(pathx, syntaxonly, printprefix+"  ", exitonerr=0):
					#print(ppx + "ERROR.")
					#return 1
				#print(ppx + "Done.\n")
			#else:
				#print(ppx + "XAS ERROR: no argument after command: asm. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
				#return 1
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
						if call(['python']+cmdobj.execstr.split(" ")+arg.split(" "))!=0:
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
