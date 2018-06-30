#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
import sys
import os
#common vars:
tritvalid="+0-pn"
asmvers='v3.0.0'
versint=(3, 0, 0)


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
nspacevar()]


#mainloop class
class mainloop:
	def __init__(self, fileobj, addrstart=libbaltcalc.mni(9)):
		self.fileobj=fileobj
		self.addrstart=addrstart
	def p0(self):
		self.fileobj.seek(0)
		print("pass 0: syntax check")
		lineno=0
		for line in self.fileobj:
			lineno+=1
			if not line.startswith("#"):
				if line.endswith("\n"):
					line=line[:-1]
				line.replace("|", ";")
				linelist=line.split(";")
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				if data=="":
					data=None
				for inst in instlist:
					if keyword in inst.keywords:
						retlist=inst.p0(data, keyword, lineno)
						if retlist[0]==1:
							if retlist[1]!=None:
								print("Syntax Error: "+retlist[1])
							else:
								print("Syntax Error!")
							return 1
					else:
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
		self.gotos={}
		print("pass 1: goto refrence label prescan")
		lineno=0
		for line in self.fileobj:
			lineno+=1
			if not line.startswith("#"):
				if line.endswith("\n"):
					line=line[:-1]
				line.replace("|", ";")
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
					if keyword in inst.keywords:
						length, nspaceadd=inst.p1(data, keyword, lineno)
						if glabel!="":
							self.gotos[glabel]=addr
						if nspaceadd!={}:
							self.gotos.update(nspaceadd)
						addr+=length
					else:
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
			if not line.startswith("#"):
				if line.endswith("\n"):
					line=line[:-1]
				line.replace("|", ";")
				linelist=line.split(";")
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				if data=="":
					data=None
				for inst in instlist:
					if keyword in inst.keywords:
						retlist=inst.p2(data, keyword, self.gotos, lineno)
						if retlist[0]==1:
							if retlist[1]!=None:
								print("Syntax Error: "+retlist[1])
							else:
								print("Syntax Error!")
							return 1
					else:
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
			if not line.startswith("#"):
				if line.endswith("\n"):
					line=line[:-1]
				line.replace("|", ";")
				linelist=line.split(";")
				keyword=linelist[0]
				try:
					data=linelist[1]
				except IndexError:
					data=None
				if data=="":
					data=None
				for inst in instlist:
					if keyword in inst.keywords:
						datinstpairs=inst.p3(data, keyword, self.gotos, lineno)
						self.datainstlist.extend(datinstpairs)
					else:
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
	def p5(self, filename):
		print("pass 5: build rom.")
		outfile=open(filename, "w")
		for item in self.datainstlist:
			inst=item[0]
			data=item[1]
			outfile.write(str(int(inst)) + "," + str(int(data)) + "\n")
		outfile.close()
		




VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")

if __name__=="__main__":
	try:
		cmd=sys.argv[1]
	except:
		cmd=None
	try:
		arg=sys.argv[2]
	except:
		arg=None
	if cmd in ['help', '-h', '--help']:
		print('''SBTCVM assembler v3
For SBTCVM Gen2-9.
help, -h, --help: this help
-v, --version: assembler version
-b, (tasmname): build tasm source file into rom at same location.
-s, --syntax (tasmname): run assembler up to final sanity checks, but don't write rom image.''')
	elif cmd in ['-v', '--version']:
		print(asmvers)
	else:
		if cmd==None:
			print("Tip: Try g2-asm.py -h for help.")
			sys.exit()
		if cmd in ['-b', '--build', '-s', '--syntax']:
			argx=arg
		else:
			argx=cmd
		if cmd in ['-s', '--syntax']:
			syntaxonly=1
		else:
			syntaxonly=0
		for filenameg in [argx, argx+".tasm", argx+".TASM"]:
			filefound=1
			if os.path.isfile(filenameg):
				pathx=filenameg
			elif os.path.isfile(os.path.join("ROMS", filenameg)):
				pathx=os.path.join("ROMS", filenameg)
			elif os.path.isfile(os.path.join("VMUSER", filenameg)):
				pathx=os.path.join("VMUSER", filenameg)
			elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
				pathx=os.path.join("VMSYSTEM", filenameg)
			elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
				pathx=os.path.join(VMSYSROMS, filenameg)
			else:
				filefound=0
			if filefound==1:
				break
		if filefound==0:
			sys.exit("source file was not found. STOP")
		basepath=pathx.split(".")[0]
		destpath=basepath+".trom"
		sourcefile=open(pathx, 'r')
		mainl=mainloop(sourcefile)
		if mainl.p0():
			sys.exit("Syntax Error (pass 0)")
		mainl.p1()
		if mainl.p2():
			sys.exit("Syntax Error (pass 2)")
		mainl.p3()
		if mainl.p4():
			sys.exit("Error: Invalid romdata! (pass 4)")
		if not syntaxonly:
			mainl.p5(destpath)
		sourcefile.close()
	