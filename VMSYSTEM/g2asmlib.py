#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
import os
import sys
from subprocess import call
tritvalid="+0-pn"
#assembler library

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



def xasparse(scrpath, syntaxonly=0):
	xasfile=open(scrpath, 'r')
	print("SBTCVM Assembly Script (XAS) v1")
	print("running: '" + scrpath + "'\n")
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
					print("----XAS subscript: '" + arg + "'")
					xasparse(pathx, syntaxonly)
					print("-Subscript Done.\n")
				else:
					sys.exit("XAS ERROR: Subscript loop error. Line: '" + str(lineno) + "' in: '" + scrpath + "'")	
			else:
				sys.exit("XAS ERROR: no argument after command: xas. Line: '" + str(lineno) + "' in: '" + scrpath + "'")	
		elif cmd=="asm":
			if arg!=None:
				pathx=iofuncts.findtrom(arg, ext=".tasm", exitonfail=1, exitmsg="XAS ERROR: source file: '" + arg + "' was not found. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
				print("assemble: '" + arg + "'")
				assemble(pathx, syntaxonly)
				print("Done.\n")
			else:
				sys.exit("XAS ERROR: no argument after command: asm. Line: '" + str(lineno) + "' in: '" + scrpath + "'")
		elif cmd=="print":
			if arg!=None:
				print("--SCRIPT: " + arg)
		elif cmd=="exit":
			break
		for cmdobj in xascmds:
			if cmd==cmdobj.xcmd:
				if cmdobj.ispython:
					if cmdobj.takesfile and arg!=None:
						if call(['python']+cmdobj.execstr.split(" ")+[arg])!=0:
							sys.exit("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "' in: '" + scrpath + "'")
					else:
						if call(['python']+cmdobj.execstr.split(" "))!=0:
							sys.exit("XAS ERROR: plugin command error! cmd:'" + cmd + "' Line: '" + str(lineno) + "' in: '" + scrpath + "'")
	print("xas finished. exiting...")
	xasfile.close()



def assemble(pathx, syntaxonly=0):
	#locate source file and extract destination basename and directory for mainloop class.
	
	basepath=pathx.rsplit(".", 1)[0]
	bpdir=os.path.dirname(basepath)
	bpname=os.path.basename(basepath)
	
	#open source file and init mainloop class
	sourcefile=open(pathx, 'r')
	mainl=mainloop(sourcefile, bpdir, bpname)
	
	#parse header
	mainl.headload()
	
	#parse each pass in order.
	if mainl.p0():
		sys.exit("Syntax Error (pass 0)")
	mainl.p1()
	if mainl.p2():
		sys.exit("Syntax Error (pass 2)")
	mainl.p3()
	if mainl.p4():
		sys.exit("Error: Invalid romdata! (pass 4)")
	if not syntaxonly:
		mainl.p5()
	sourcefile.close()


#classes and instances for instructions

#basic instruction. literally any instruction that uses this automatically supports goto refrence carrot stntax (keyword;>gotorefrence)
class instruct:
	def __init__(self, keywords, opcode):
		self.keywords=keywords
		self.prefixes=[]
		self.opcode=int(opcode)
	def p0(self, data, keyword, lineno):
		if data==None:
			return 0, None
		elif data.startswith(">"):
			return 0, None
		elif data.startswith("10x"):
			try:
				int(data[3:])
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error!"
			
		else:
			if len(data)>9:
				return 1, keyword+": Line: " + str(lineno) + ": string too large!"
			for char in data:
				
				if char not in tritvalid:
					return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string!"
		return 0, None
	#return length in words of memory. needed here for goto refrence label parsing!
	def p1(self, data, keyword, lineno):
		return 1, {}
	#second syntax check pass:
	def p2(self, data, keyword, gotos, lineno):
		if data==None:
			return 0, None
		elif data.startswith(">"):
			try:
				gotos[data[1:]]
			except KeyError:
				return 1, keyword+": Line " + str(lineno) + ": Nonexistant goto refrence!"
				
		return 0, None
	#should return two signed ints or btint objects.
	def p3(self, data, keyword, gotos, lineno):
		if data==None:
			return [[self.opcode, 0]]
		elif data.startswith("10x"):
			return [[self.opcode, int(data[3:]), lineno]]
		elif data.startswith(">"):
			return [[self.opcode, gotos[data[1:]], lineno]]
		else:
			return [[self.opcode, libbaltcalc.btint(data), lineno]]

class rawinst:
	def __init__(self):
		self.keywords=["raw"]
		self.prefixes=[]
	def p0(self, datafull, keyword, lineno):
		if datafull==None:
			return 1, keyword+": Line: " + str(lineno) + ": 'raw' requires TWO numeric arguments! raw;arga,argb"
		datalist=datafull.split(",")
		if len(datalist)!=2:
			return 1, keyword+": Line: " + str(lineno) + ": 'raw' requires TWO numeric arguments! raw;arga,argb"
		for data in datalist:
			if data.startswith(">"):
				continue
			elif data.startswith("10x"):
				try:
					int(data[3:])
				except ValueError:
					return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error! (" + data + ")"
				
			else:
				if len(data)>9:
					return 1, keyword+": Line: " + str(lineno) + ": string too large! (" + data + ")"
				for char in data:
					
					if char not in tritvalid:
						return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string! (" + data + ")"
		return 0, None
	#return length in words of memory. needed here for goto refrence label parsing!
	def p1(self, data, keyword, lineno):
		return 1, {}
	#second syntax check pass:
	def p2(self, datafull, keyword, gotos, lineno):
		datalist=datafull.split(",")
		for data in datalist:
			if data.startswith(">"):
				try:
					gotos[data[1:]]
				except KeyError:
					return 1, keyword+": Line " + str(lineno) + ": Nonexistant goto refrence! (" + data + ")"
				
		return 0, None
	#should return two signed ints or btint objects.
	def p3(self, data, keyword, gotos, lineno):
		datalist=data.split(",")
		data1=datalist[0]
		data2=datalist[1]
		if data1.startswith("10x"):
			data1res=int(data1[3:])
		elif data1.startswith(">"):
			data1res=gotos[data1[1:]]
		else:
			data1res=libbaltcalc.btint(data2)
		if data2.startswith("10x"):
			data2res=int(data2[3:])
		elif data2.startswith(">"):
			data2res=gotos[data2[1:]]
		else:
			data2res=libbaltcalc.btint(data2)
		
		
		return [[data1res, data2res, lineno]]

class nspacevar:
	def __init__(self):
		self.keywords=[]
		self.prefixes=['v>']
	def p0(self, data, keyword, lineno):
		if not len(keyword)>2:
			return 1, keyword+": Line: " + str(lineno) + ": No variable name after prefix! (v>varname)"
		if data==None:
			return 0, None
		elif data.startswith(">"):
			return 0, None
		elif data.startswith("10x"):
			try:
				int(data[3:])
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error!"
			
		else:
			if len(data)>9:
				return 1, keyword+": Line: " + str(lineno) + ": string too large!"
			for char in data:
				
				if char not in tritvalid:
					return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string!"
		return 0, None
	#return length in words of memory, and if any, custom namespace entries. needed here for goto refrence label parsing!
	def p1(self, data, keyword, lineno):
		if data==None:
			return 0, {keyword[2:]: 0}
		elif data.startswith("10x"):
			return 0, {keyword[2:]: int(data[3:])}
		elif data.startswith(">"):
			return 0, {keyword[2:]: gotos[data[1:]]}
		else:
			return 0, {keyword[2:]: libbaltcalc.btint(data)}
	#second syntax check pass:
	def p2(self, data, keyword, gotos, lineno):
		if data==None:
			return 0, None
		elif data.startswith(">"):
			try:
				gotos[data[1:]]
			except KeyError:
				return 1, keyword+": Line " + str(lineno) + ": Nonexistant goto refrence!"
				
		return 0, None
	#should return two signed ints or btint objects, or if no output, an empty list.
	def p3(self, data, keyword, gotos, lineno):
		return []
		



#master keyword parser object list:
instlist=[instruct(["null"], 0),
rawinst(),
instruct(["setreg1"], -9841),
instruct(["setreg2"], -9840),
instruct(["copy2to1"], -9839),
instruct(["copy1to2"], -9838),
instruct(["regswap"], -9837),
instruct(["invert1"], -9836),
instruct(["invert2"], -9835),
instruct(["stop"], -9000),
instruct(["add"], -9800),#add instructions
instruct(["add2"], -9799),
instruct(["adddata1"], -9798),
instruct(["adddata2"], -9797),
instruct(["sub"], -9796),#sub instructions
instruct(["sub2"], -9795),
instruct(["subdata1"], -9794),
instruct(["subdata2"], -9793),
instruct(["mul"], -9792),#mul instructions
instruct(["mul2"], -9791),
instruct(["muldata1"], -9790),
instruct(["muldata2"], -9789),
instruct(["div"], -9788),#div instructions
instruct(["div2"], -9787),
instruct(["divdata1"], -9786),
instruct(["divdata2"], -9785),

nspacevar()]

nameallowed="abcdefghijklmnopqrstuvwxyz_-1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"

defaultnspace={}

#mainloop class
class mainloop:
	def __init__(self, fileobj, basepath, destname, addrstart=libbaltcalc.mni(9)):
		self.fileobj=fileobj
		self.addrstart=addrstart
		self.destext=".trom"
		self.basepath=basepath
		self.destname=destname
	
	def headload(self):
		#header load.
		self.fileobj.seek(0)
		mode="trom"
		self.nsp=0
		self.gotos=dict(defaultnspace)
		self.doout=1
		self.romdestname=self.destname
		self.nspdestname=self.destname
		for line in self.fileobj:
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
			
			if line.startswith("head-mode="):
				mode=line.split("=")[1]
			
			if line.startswith("head-nspout="):
				if '1' in line.split("=")[1]:
					self.nsp=1
			
			if line.startswith("head-nspin="):
				nspname=line.split("=")[1]
				nspobj=iofuncts.loadtrom(nspname, ext=".nsp", exitonfail=1, exitmsg="ERROR: header: head-nspin: nonexistant nsp file! '" + nspname + "'")
				for linex in nspobj:
					linex=linex.replace("\n", "")
					name, value = linex.split(";")
					self.gotos[name]=int(value)
				print("-Include namespace file: '" + nspname + "'")
				
			if line.startswith("head-rname="):
				self.romdestname=line.split("=")[1]
				if len(self.romdestname)==0:
					sys.exit("ERROR: header: head-rname: name must be at least 1 character long.")
				for char in self.romdestname:
					if char not in nameallowed:
						sys.exit("ERROR: header: head-rname: invalid char '" + char + "' in name: '" + self.romdestname + "'")
				print("Header: rom name override: '" + self.romdestname + "'")
			if line.startswith("head-nspname="):
				self.nspdestname=line.split("=")[1]
				if len(self.nspdestname)==0:
					sys.exit("ERROR: header: head-nspname: name must be at least 1 character long.")
				for char in self.nspdestname:
					if char not in nameallowed:
						sys.exit("ERROR: header: head-nspname: invalid char '" + char + "' in name: '" + self.nspdestname + "'")
				print("Header: nsp name override: '" + self.nspdestname + "'")
		
		#header framework for future alternate assemble modes. i.e. different starting offsets, etc.
		if mode=="trom":
			self.addrstart=libbaltcalc.mni(9)
			self.destext=".trom"
			print("Header: head-mode: trom (default)")
		elif mode=="vars":
			self.addrstart=libbaltcalc.mni(9)
			self.destext=".trom"
			self.doout=0
			print("Header: head-mode: vars (nspace vars only)")
		else:
			sys.exit("ERROR: header: head-mode: Invalid mode: '" + mode + "'")
		#set assembler rom output filename.
		self.romoutput=os.path.join(self.basepath, self.romdestname+self.destext)
		if self.nsp==1:
			self.nspfile=os.path.join(self.basepath, self.nspdestname+'.nsp')
			self.nspdict={}
		else:
			self.nspfile=None
			self.nspdict=None
	def p0(self):
		self.fileobj.seek(0)
		print("pass 0: syntax check")
		lineno=0
		for line in self.fileobj:
			lineno+=1
			if not line.startswith("#") and not line.startswith("head-"):
				#strip newlines & end-of-line comments
				if line.endswith("\n"):
					line=line[:-1]
				if '#' in line:
					line=line.rsplit("#", 1)[0]
				line.replace("|", ";")
				#parse
				linelist=line.split(";")
				
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				if data=="":
					data=None
				for inst in instlist:
					#normal keywords
					if keyword in inst.keywords:
						retlist=inst.p0(data, keyword, lineno)
						if retlist[0]==1:
							if retlist[1]!=None:
								print("Syntax Error: "+retlist[1])
							else:
								print("Syntax Error!")
							return 1
					else:
						#prefix keywords
						for pattern in inst.prefixes:
							if keyword.startswith(pattern):
								retlist=inst.p0(data, keyword, lineno)
								if retlist[0]==1:
									if retlist[1]!=None:
										print("Syntax Error: "+retlist[1])
									else:
										print("Syntax Error!")
									return 1
		return 0
	def p1(self):
		self.fileobj.seek(0)
		
		print("pass 1: goto reference label prescan")
		lineno=0
		for line in self.fileobj:
			lineno+=1
			if not line.startswith("#") and not line.startswith("head-"):
				#strip newlines & end-of-line comments
				if line.endswith("\n"):
					line=line[:-1]
				if '#' in line:
					line=line.rsplit("#", 1)[0]
				line.replace("|", ";")
				#parse
				linelist=line.split(";")
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				try:
					glabel=linelist[2]
				except IndexError:
					glabel=None
				if data=="":
					data=None
				addr=self.addrstart
				for inst in instlist:
					#normal keywords
					if keyword in inst.keywords:
						length, nspaceadd=inst.p1(data, keyword, lineno)
						if glabel!="":
							self.gotos[glabel]=addr
							if self.nspfile!=None:
								self.nspdict[glabel]=addr
						if nspaceadd!={}:
							self.gotos.update(nspaceadd)
							if self.nspfile!=None:
								for f in nspaceadd:
									self.nspdict.update(nspaceadd)
						addr+=length
					else:
						#prefix keywords
						for pattern in inst.prefixes:
							if keyword.startswith(pattern):
								length, nspaceadd=inst.p1(data, keyword, lineno)
								if glabel!="":
									self.gotos[glabel]=addr
								if nspaceadd!={}:
									self.gotos.update(nspaceadd)
									if self.nspfile!=None:
										for f in nspaceadd:
											self.nspdict.update(nspaceadd)
								addr+=length
	def p2(self):
		self.fileobj.seek(0)
		print("pass 2: post-prescan syntax check")
		lineno=0
		for line in self.fileobj:
			lineno+=1
			if not line.startswith("#") and not line.startswith("head-"):
				#strip newlines & end-of-line comments
				if line.endswith("\n"):
					line=line[:-1]
				if '#' in line:
					line=line.rsplit("#", 1)[0]
				
				line.replace("|", ";")
				#parse
				linelist=line.split(";")
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				if data=="":
					data=None
				for inst in instlist:
					#normal keywords
					if keyword in inst.keywords:
						retlist=inst.p2(data, keyword, self.gotos, lineno)
						if retlist[0]==1:
							if retlist[1]!=None:
								print("Syntax Error: "+retlist[1])
							else:
								print("Syntax Error!")
							return 1
					else:
						#prefix keywords
						for pattern in inst.prefixes:
							if keyword.startswith(pattern):
								retlist=inst.p2(data, keyword, self.gotos, lineno)
								if retlist[0]==1:
									if retlist[1]!=None:
										print("Syntax Error: "+retlist[1])
									else:
										print("Syntax Error!")
									return 1
		return 0
	def p3(self):
		self.datainstlist=[]
		self.fileobj.seek(0)
		print("pass 3: main parse pass")
		lineno=0
		for line in self.fileobj:
			lineno+=1
			if not line.startswith("#") and not line.startswith("head-"):
				#strip newlines & end-of-line comments
				if line.endswith("\n"):
					line=line[:-1]
				if '#' in line:
					line=line.rsplit("#", 1)[0]
				line.replace("|", ";")
				
				#parse
				linelist=line.split(";")
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				if data=="":
					data=None
				for inst in instlist:
					#normal keywords
					if keyword in inst.keywords:
						datinstpairs=inst.p3(data, keyword, self.gotos, lineno)
						self.datainstlist.extend(datinstpairs)
					else:
						#prefix keywords
						for pattern in inst.prefixes:
							if keyword.startswith(pattern):
								datinstpairs=inst.p3(data, keyword, self.gotos, lineno)
								self.datainstlist.extend(datinstpairs)
	def p4(self):
		print("pass 4: Rom validity check")
		for item in self.datainstlist:
			#print(item)
			inst=int(item[0])
			data=int(item[1])
			if inst<libbaltcalc.mni(9) or inst>libbaltcalc.mpi(9):
				print("Out of range instruction word found!")
				print("source line: " + str(item[2]))
				return 1
			if data<libbaltcalc.mni(9) or data>libbaltcalc.mpi(9):
				print("Out of range data word found!")
				print("source line: " + str(item[2]))
				return 1
		if len(self.datainstlist)>19683:
			print("Memory Space Overflow!")
			return 1
		return 0
	def p5(self):
		if self.nspfile!=None:
			print("pass 5: generate nsp file.")
			nspout=open(self.nspfile, 'w')
			for f in self.nspdict:
				if f != None:
					nspout.write(str(f) + ";" + str(int(self.nspdict[f])) + "\n")
			nspout.close()
		if self.doout==1:
			print("pass 5: build rom.")
			outfile=open(self.romoutput, 'w')
			for item in self.datainstlist:
				inst=item[0]
				data=item[1]
				outfile.write(str(int(inst)) + "," + str(int(data)) + "\n")
			outfile.close()