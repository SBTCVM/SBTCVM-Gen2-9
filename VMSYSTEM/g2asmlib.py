#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys
tritvalid="+0-pn"
#assembler library


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
		for line in self.fileobj:
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
			
			if line.startswith("head-mode="):
				mode=line.split("=")[1]
			
			if line.startswith("head-rname="):
				self.destname=line.split("=")[1]
				if len(self.destname)==0:
					sys.exit("ERROR: header: head-rname: name must be at least 1 character long.")
				for char in self.destname:
					if char not in nameallowed:
						sys.exit("ERROR: header: head-rname: invalid char '" + char + "' in name: '" + self.destname + "'")
				print("Header: rname override: '" + self.destname + "'")
		
		#header framework for future alternate assemble modes. i.e. different starting offsets, etc.
		if mode=="trom":
			self.addrstart=libbaltcalc.mni(9)
			self.destext=".trom"
			print("Header: head-mode: trom (default)")
			self.gotos=dict(defaultnspace)
		else:
			sys.exit("ERROR: header: head-mode: Invalid mode: '" + mode + "'")
		#set assembler rom output filename.
		self.romoutput=os.path.join(self.basepath, self.destname+self.destext)
	
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
						if nspaceadd!={}:
							self.gotos.update(nspaceadd)
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
		print("pass 5: build rom.")
		outfile=open(self.romoutput, "w")
		for item in self.datainstlist:
			inst=item[0]
			data=item[1]
			outfile.write(str(int(inst)) + "," + str(int(data)) + "\n")
		outfile.close()