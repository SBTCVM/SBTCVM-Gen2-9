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
xasvers='v2.1.0'
versint=(2, 1, 0)

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
  
'''
  
  
 
ftype_descs_verbose={"trom": "SBTCVM Ternary ROM",
"tasm": "SBTCVM assembly source code.",
"tas0": "SBTCVM assembly loadable module.",
"nsp": "SBTCVM assembly compile-time viariable library.",
"stnp": "SSTNPL source code.",
"stnpmfs": "SSTNPL module manifest.",
"diskmap": "Diskedit disk description map.",
"tdsk1": "Format 1 SBTVDI disk image.",
"xas": "XAS portable build script."}

#these descriptions should be all the same width.
ftype_descs_fixed={
   "trom": "SBTCVM Ternary ROM      : ",
   "tasm": "SBTCVM-ASM source file  : ",
   "tas0": "SBTCVM-ASM tas0 Module  : ",
    "nsp": "SBTCVM-ASM variable lib : ",
   "stnp": "SSTNPL Source code      : ",
"stnpmfs": "SSTNPL Module Manifest  : ",
"diskmap": "Diskedit disk blueprints: ",
  "tdsk1": "Disk image (format 1)   : ",
    "xas": "XAS build script        : "}
    
ftype_descs_fixed_short={
   "trom": "trom    : ",
   "tasm": "tasm    : ",
   "tas0": "tasm    : ",
    "nsp": "nsp     : ",
   "stnp": "stnp    : ",
"stnpmfs": "stnpmfs : ",
"diskmap": "diskmap : ",
  "tdsk1": "tdsk1   : ",
    "xas": "xas     : "}
 
#generic fileinfo printer (used by find and list)
def fileinfo(filen, pathx, sublist=0):
	if sublist:
		prfx="    "
	else:
		prfx=" "
		
	for ext in ftype_descs_fixed_short:
		if filen.lower().endswith("."+ext):
			print(prfx + ftype_descs_fixed_short[ext] + pathx)
			return
	return

autodirexts=["trom", "nsp", "stnp", "xas", "tdsk1", "diskmap", "stnpmfs", "tas0", "tasm"]

#shell input function
def getinput():
	try:
		try:
			return raw_input('XAS>')
		except NameError:
			return input('XAS>')
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
			print(prfx + " -DIR-   : " + pathx)
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
					autodstr=""
					for filesub in os.listdir(joinedpath):
						#Detect SBTCVM smart app directories.
						if filesub.startswith("auto_") and search.lower() in filen.lower():
							if "." in filesub:
								filesub_ext=filesub.split(".")[1].lower()
								if filesub_ext in autodirexts:
									autodstr=(autodstr+filesub_ext.upper()+", ")
						else:
							matcherprint(filesub, search,  filen + "+" + filesub, sublist=1)
					if autodstr!="":
						print("  >autodir: " + autodstr)
				
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
				print(" -DIR-   : " + filen)
				#Detect SBTCVM smart app directories.
				#if pathdesc in iofuncts.smartpaths:
				
				autodstr=""
				for filesub in os.listdir(os.path.join(realpath, filen)):
					if filesub.startswith("auto_"):
						if "." in filesub:
							filesub_ext=filesub.split(".")[1].lower()
							if filesub_ext in autodirexts:
								autodstr=(autodstr+filesub_ext.upper()+", ")
				if autodstr!="":
					print("      autodir: " + autodstr)
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

##Debug variables.
shelldebug_plugcmdid=False
#Debug command. (Intended to help debug interactive mode as it becomes more advanced.)
def debugcmd(arg):
	global shelldebug_plugcmdid
	if arg=="options":
		print("""DEBUG COMMANDS: (BOOL options accept 1/true/on and 0/false/off)
    plugcmdid [BOOL]: Plugin Command Identifiers
    status: print XAS shell status""")
	arglist=arg.split(" ")
	try:
		dcmd=arglist[0]
		darg=arglist[1]
	except IndexError:
		dcmd=arglist[0]
		darg=None
	if dcmd=="plugcmdid":
		if darg=="1" or darg.lower()=="true" or darg.lower()=="on":
			shelldebug_plugcmdid=True
		elif darg=="0" or darg.lower()=="false" or darg.lower()=="off":
			shelldebug_plugcmdid=False
		elif darg==None:
			print("please specify 'debug plugcmdid [1/0]'")
			return
	if dcmd=="status":
		print("--DEBUG OPTIONS--")
		print("plugcmdid: " + str(shelldebug_plugcmdid))
		

histfilepath=os.path.join(*["vmuser", "CFG", "XAS_HISTORY.txt"])
def posix_history_helper():
	if not os.path.isfile(histfilepath):
		print("Creating history file as: '" + histfilepath + "'")
		open(histfilepath, "w").close()
	readline.read_history_file(histfilepath)

#interactive interpreter
def xasshell():
	global shelldebug
	print(shellwelcome)
	try:
		global readline
		import readline
		posix_history_helper()
		readline_inuse=True
	except ImportError:
		print("Failed to load readline. Note: XAS will still work!")
		readline_inuse=False
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
		
		if cmd=="debug":
			if arg==None:
				print("Please see 'debug options' for XAS debug commands.")
			else:
				debugcmd(arg)
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
		elif cmd=="history":
			if not readline_inuse:
				print("ERROR: readline was not loaded. History support disabled.")
			else:
				if arg=="clear":
					readline.clear_history()
					print("History Cleared.")
				if arg=="list":
					curline=1
					while curline!=readline.get_current_history_length()+1:
						print(readline.get_history_item(curline))
						curline+=1
					
				if arg==None:
					print("please see 'help history' for usage.")
		elif cmd=="about":
			print(abouttext)
		elif cmd in ["ver", "version", "info"]:
			print(verinfo)
		elif cmd=="exit":
			if readline_inuse:
				readline.write_history_file(histfilepath)
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
						if shelldebug_plugcmdid:
							print("command plugin (is python script)")
						if cmdobj.takesfile and arg!=None:
							if shelldebug_plugcmdid:
								print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "' file argument: '" + arg + "'\n-------------")
							if call(['python']+cmdobj.execstr.split(" ")+arg.split(" "))!=0:
								print("XAS ERROR: plugin command error! cmd:'" + cmd + "'")
							#print(shellwelcome)
						else:
							if shelldebug_plugcmdid:
								print("plugin cmd: '" + cmd + "' exec: '" + cmdobj.execstr + "'\n-------------")
							if call(['python']+cmdobj.execstr.split(" "))!=0:
								print("XAS ERROR: plugin command error! cmd:'" + cmd + "'")
							#print(shellwelcome)
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
	srcdir=os.path.dirname(scrpath)
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
		
		if arg!=None:
			if '%xwd%' in arg:
				arg=arg.replace('%xwd%', srcdir)
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
