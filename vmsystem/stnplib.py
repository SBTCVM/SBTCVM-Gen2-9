#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys
#from subprocess import call
from . import libtextcon as tcon
from . import g2asmlib
from . import iofuncts
#variable type constants
nptype_int=2
nptype_str=3#not used
nptype_label=4
nptype_table=5
nptype_const=6
nptype_macro=7


#SSTNPL compiler main routine library.

stnpvers='v0.4.0'
versint=(0, 4, 0)

class npvar:
	def __init__(self, vname, vdata, vtype=nptype_int, frommodule=0):
		self.vname=vname
		self.vdata=vdata
		self.vtype=vtype
		self.frommodule=frommodule

tritvalid="+0-pn"
bal9_valid="43210ZYXW"

bal27_valid="DCBA9876543210ZYXWVUTSRQPNM"

varvalid="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"
reservednames=[""]

builtin_constants={"true": "10x1", "false": "10x0"}
constants=dict(builtin_constants)
localconstants={}
def set_const(name, value):
	constants[name]=value
	localconstants[name]=value

fcon_stack=[]

fcon_id_cnt=0

#flow control Logic helpers

def fcon_begin(loop=False):
	global fcon_id_cnt
	fcon_id_cnt+=1
	if loop:
		fcon_strx="flowloop--con-x-"+str(fcon_id_cnt)
	else:
		fcon_strx="flow--con-x-"+str(fcon_id_cnt)
	fcon_stack.insert(0, fcon_strx)
	return fcon_strx

def fcon_loopback():
	
	return fcon_stack[0]+"--start"

def fcon_break():
	return fcon_stack[0]

def fcon_end():
	return fcon_stack.pop(0)

def fcon_top():
	fx=fcon_stack[0]
	#if fx.startswith("flowloop--"):
	return fx+"--start"
	#return fx

#flow control logic syntax helpers

fsyntax_stack=[]

def fsyntax_begin(lineno, info):
	fsyntax_stack.insert(0, "Block: type '" + info + "' on line '" + str(lineno) + "'")

def fsyntax_break(lineno, info):
	if fsyntax_stack==[]:
		return 1, "Break: '" + info + "' on line '" + str(lineno) + "', is not within a block."
def fsyntax_top(lineno, info):
	if fsyntax_stack==[]:
		return 1, "End: '" + info + "' on line '" + str(lineno) + "', is not within a block."

def fsyntax_end(lineno, info):
	if fsyntax_stack==[]:
		return 1, "End: '" + info + "' on line '" + str(lineno) + "', is not within a block."
	fsyntax_stack.pop(0)

class in_fcon_break:
	def __init__(self):
		self.keywords=["break"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		retx=fsyntax_break(lineno, keyword)
		
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("goto;>" + fcon_break() + "\n")
		return

class in_fcon_top:
	def __init__(self):
		self.keywords=["top"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		retx=fsyntax_top(lineno, keyword)
		
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("goto;>" + fcon_top() + "\n")
		return

class in_fcon_loop:
	def __init__(self):
		self.keywords=["loop"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		fsyntax_begin(lineno, keyword)
		
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		blockname=fcon_begin(loop=True)
		destobj.write('''#unconditional loop
zerosize;;''' + fcon_loopback() + "\n")
		
		return

class in_fcon_ignore:
	def __init__(self):
		self.keywords=["ignore"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		fsyntax_begin(lineno, keyword)
		fsyntax_break(lineno, keyword)
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		blockname=fcon_begin(loop=False)
		destobj.write('''#ignore block
zerosize;;''' + fcon_loopback() + "\n")
		destobj.write("goto;>" + fcon_break() + "\n")
		return

class in_fcon_begin:
	def __init__(self):
		self.keywords=["begin"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		fsyntax_begin(lineno, keyword)
		
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		blockname=fcon_begin(loop=False)
		destobj.write('''#unconditional begin
zerosize;;''' + fcon_loopback() + "\n")
		return
class in_fcon_end:
	def __init__(self):
		self.keywords=["end"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		retx=fsyntax_end(lineno, keyword)
		if retx!=None:
			return retx
		
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		if fcon_break().startswith("flowloop"):
			destobj.write("goto;>" + fcon_loopback() + "\n")
		destobj.write("zerosize;;" + fcon_end() + "\n")
		return


#variable creation statement
class in_var:
	def __init__(self):
		self.keywords=["var"]
	def p0(self, args, keyword, lineno):
		argsplit=args.split("=", 1)
		
		if len(argsplit)!=2:
			return 1, "must specify varname=valiue! '" + str(lineno) + "'"
		data=argsplit[1]
		name=argsplit[0]
		for char in name:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in variable name! '" + char + "'"
		if name in reservednames:
			return 1, keyword+": Line: " + str(lineno) + ": variable name: '" + args + "' Is reserved."
		if data.replace("@", "10x").startswith("10x"):
			try:
				int(data.replace("@", "10x")[3:])
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error!"
		#this syntax will make this var equal the encoding data of the specified character.
		elif data.startswith(":"):
			if len(data)<2:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify character"
		else:
			if len(data.replace("*", ""))>9:
				return 1, keyword+": Line: " + str(lineno) + ": string too large!"
			for char in data.replace("*", ""):
				
				if char not in tritvalid:
					return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string!"
		return 0, None
	def p1(self, args, keyword, lineno):
		argsplit=args.split("=", 1)
		name=argsplit[0]
		data=argsplit[1]
		if data.startswith("*"):
			data=data.replace("*", "")
		if data.startswith("@"):
			data=data.replace("@", "10x")
		return [npvar(name, data, vtype=nptype_int)]
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		return



class in_const:
	def __init__(self):
		self.keywords=["const"]
	def p_const(self, args, keyword, lineno):
		argsplit=args.split("=", 1)
		
		if len(argsplit)!=2:
			return 1, "must specify varname=valiue! '" + str(lineno) + "'"
		data=argsplit[1]
		name=argsplit[0]
		for char in name:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in constant name! '" + char + "'"
		if data.replace("@", "10x").startswith("10x"):
			try:
				int(data.replace("@", "10x")[3:])
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error!"
		#this syntax will make this var equal the encoding data of the specified character.
		elif data.startswith(":"):
			if len(data)<2:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify character"
		else:
			if len(data.replace("*", ""))>9:
				return 1, keyword+": Line: " + str(lineno) + ": string too large!"
			for char in data.replace("*", ""):
				
				if char not in tritvalid:
					return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string!"
		
		if data.startswith("*"):
			data=data.replace("*", "")
		if data.startswith("@"):
			data=data.replace("@", "10x")
		return 0, [npvar(name, data, vtype=nptype_const)]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		return



class in_include:
	def __init__(self):
		self.keywords=["include"]
		self.varspacenames=[]
	def pmacro(self, args, keyword, lineno):
		
		#basic check
		try:
			basename, foo, varprefix = args.split(" ")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": must specify 'include [modulename] as [varspace name]"
		print("MODULE LOAD: PRESCAN: LINE " + str(lineno) + ": " + basename + " as " + varprefix)
		#varspace name checks
		if varprefix=="":
			return 1, keyword+": Line: " + str(lineno) + ": varspace name MUST NOT BE BLANK"
		if varprefix in self.varspacenames:
			return 1, keyword+": Line: " + str(lineno) + ": varspace name '" + varprefix + "' already used. DUPLICATES NOT ALLOWED."
		for char in varprefix:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in varspace name! '" + char + "'"
				
		self.varspacenames.extend([varprefix])
		#file existence checks:
		if iofuncts.findtrom(basename, ext=".tas0", exitonfail=0, dirauto=1)==None:
			return 1, keyword+": Line: " + str(lineno) + ": '" + basename + "': UNABLE TO FIND MODULE's '*.tas0' ASSEMBLER MODULE FILE."
		if iofuncts.findtrom(basename, ext=".stnpmfs", exitonfail=0, dirauto=1)==None:
			return 1, keyword+": Line: " + str(lineno) + ": '" + basename + "': UNABLE TO FIND MODULE's '*.stmpmfs' VARIABLE MANIFEST FILE."
		
		#check manifest file for errors/corrupted data during first error check pass.
		fname=iofuncts.findtrom(basename, ext=".stnpmfs", exitonfail=0, dirauto=1)
		fileobj=open(fname, "r")
		varlist=[]
		for f in fileobj:
			f=f.replace("\n", "")
			if ";" in f:
				try:
					flist=f.split(";", 2)
					if flist[0]=="macro":
						try:
							name=varprefix + "." + flist[1]
							code=flist[2]
						except ValueError:
							return 1, keyword+": Line: " + str(lineno) + ": '" + basename + "': MALFORMED MACRO ENTRY IN MANIFEST\n    '" + f + "'"
						nvar=npvar(name, code, vtype=nptype_macro)
						nvar.modprefix=varprefix + "."
						varlist.extend([nvar])
				except IndexError:
					return 1, keyword+": Line: " + str(lineno) + ": '" + basename + "': MALFORMED DATAFIELD IN MANIFEST\n    '" + f + "'"
		fileobj.close()
		return varlist
	def p0(self, args, keyword, lineno):
		return 0, None
	def p_const(self, args, keyword, lineno):
		
		basename, foo, varprefix = args.split(" ")
		#check manifest file for errors/corrupted data during first error check pass.
		fname=iofuncts.findtrom(basename, ext=".stnpmfs", exitonfail=0, dirauto=1)
		fileobj=open(fname, "r")
		varlist=[]
		for f in fileobj:
			f=f.replace("\n", "")
			if ";" in f:
				try:
					flist=f.split(";")
					if flist[0]=="int9":
						npvar(flist[1], flist[2], vtype=nptype_int)
					if flist[0]=="const":
						varlist.extend([npvar(varprefix + "." + flist[1], flist[2], vtype=nptype_const, frommodule=1)])

					if flist[0]=="label":
						npvar(flist[1], None, vtype=nptype_label)
					if flist[0]=="table":
						try:
							npvar(flist[1], [int(flist[2]), int(flist[3])], vtype=nptype_table)
						except ValueError:
							return 1, keyword+": Line: " + str(lineno) + ": '" + basename + "': MALFORMED TABLE SIZE FIELD IN MANIFEST\n    '" + f + "'"
				except IndexError:
					return 1, keyword+": Line: " + str(lineno) + ": '" + basename + "': MALFORMED DATAFIELD IN MANIFEST\n    '" + f + "'"
		fileobj.close()
		return 0, varlist
	def p1(self, args, keyword, lineno):
		basename, foo, varprefix = args.split(" ")
		varlist=[]
		print("MODULE LOAD: MANIFEST: LINE " + str(lineno) + ": " + basename + " as " + varprefix)
		fname=iofuncts.findtrom(basename, ext=".stnpmfs", exitonfail=0, dirauto=1)
		fileobj=open(fname, "r")
		for f in fileobj:
			f=f.replace("\n", "")
			if ";" in f:
				flist=f.split(";")
				if flist[0]=="int9":
					varlist.extend([npvar(varprefix + "." + flist[1], flist[2], vtype=nptype_int, frommodule=1)])
				#if flist[0]=="const":
				#	varlist.extend([npvar(varprefix + "." + flist[1], flist[2], vtype=nptype_const, frommodule=1)])
				if flist[0]=="label":
					varlist.extend([npvar(varprefix + "." + flist[1], None, vtype=nptype_label, frommodule=1)])
				if flist[0]=="table":
					varlist.extend([npvar(varprefix + "." + flist[1], [flist[2], flist[3]], vtype=nptype_table, frommodule=1)])
		fileobj.close()
		
		return varlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		basename, foo, varprefix = args.split(" ")
		print("MODULE LOAD: TAS0: LINE " + str(lineno) + ": " + basename + " as " + varprefix)
		destobj.write('#module include: line ' + str(lineno) + ": " + basename + " as " + varprefix + "\n")
		destobj.write('includeas;' + basename + "," + varprefix + "\n")
		
		return


#value command, (often used with set)
class in_val:
	def __init__(self):
		self.keywords=["val"]
	def p0(self, args, keyword, lineno):
		if args.replace("@", "10x").startswith("10x"):
			try:
				int(args.replace("@", "10x")[3:])
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error!"
		elif args.startswith(":"):
			if len(args)<2:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify character"
		else:
			if len(args.replace("*", ""))>9:
				return 1, keyword+": Line: " + str(lineno) + ": string too large!"
			for char in args.replace("*", ""):
				
				if char not in tritvalid:
					return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string!"
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		if args.startswith("*"):
			args=args.replace("*", "")
		if args.startswith("@"):
			args=args.replace("@", "10x")
		destobj.write("#val (used with set to change variable value during runtime.)\nsetreg1;" + args + "\n")
		return

#labels (i.e. for goto & gsub)
class in_label:
	def __init__(self):
		self.keywords=["label"]
	def p0(self, args, keyword, lineno):
		for char in args:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in label! '" + char + "'"
		if args in reservednames:
			return 1, keyword+": Line: " + str(lineno) + ": label name: '" + args + "' Is reserved."
		return 0, None
	def p1(self, args, keyword, lineno):
		return [npvar(args, None, vtype=nptype_label)]
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#label\n" + "zerosize;;" + args+"--label" + "\n")
		return
		


#used in tandem with tstr, prline, and/or tdat statements to create tables.
class in_table:
	def __init__(self):
		self.keywords=["table"]
	def p0(self, args, keyword, lineno):
		try:
			args, w, h= args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": MUST SPECIFY [name],[width],[height] as arguments."
		
		try:
			w=int(w)
			if w<0:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid width argument. must be positive."
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": Invalid width argument. must be decimal."
		
		try:
			h=int(h)
			if h<0:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid width argument. must be positive."
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": Invalid width argument. must be decimal."
		
		
		for char in args:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in table! '" + char + "'"
		if args in reservednames:
			return 1, keyword+": Line: " + str(lineno) + ": table name: '" + args + "' Is reserved."
		return 0, None
	def p1(self, args, keyword, lineno):
		args, w, h= args.split(",")
		return [npvar(args, [int(w), int(h)], vtype=nptype_table)]
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		args, w, h= args.split(",")
		destobj.write("#table width=" + w + ", height=" + h + "\n" + "zerosize;;" + args+"--table" + "\n")
		return
		

#wrapper for SBTCVM Assembly's debug marker.
class in_marker:
	def __init__(self):
		self.keywords=["marker"]
	def p0(self, args, keyword, lineno):
		if args=="":
			return 1, keyword+": Line: " + str(lineno) + ": Unnamed Debug Marker!"
		return 0, None
	def p1(self, args, keyword, lineno):
		return [npvar(args, None, vtype=nptype_label)]
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#marker\n" + "marker;" + args + "' .stnp line: '" + str(lineno) + "\n")
		return

#inline assembly
class in_rawasm:
	def __init__(self):
		self.keywords=["a", "asm"]
	def p0(self, args, keyword, lineno):
		print("Embedded assembly code at line: '" + str(lineno) + "': " + args)
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#___RAW ASSEMBLY CODE___\n#_______NOTE: this corresponds to SSTNPL source line #" + str(lineno) + "\n" + args + "#SSTNPL Source Line: '" + str(lineno) + "' \n")
		return

#common command class for basic integer-variable-driven commands.
class in_intcommon1:
	def __init__(self, keywords, prearg, postarg, comment):
		self.keywords=keywords
		self.prearg=prearg
		self.postarg=postarg
		self.comment=comment
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		if args in valid_nvars:
			return 0, None
		else:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + self.comment + "\n" + self.prearg + args + self.postarg)
		return
		


class in_for:
	def __init__(self):
		self.keywords=["for"]
	def p0(self, args, keyword, lineno):
		try:
			var, indummy, formode, modeargs = args.split(" ")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid argument sequence.'" + args + "'"
		try:
			start, end, step = modeargs.split(",")
		except IndexError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid argument sequence.'" + args + "'"
		
		if formode not in ["urange", "drange", "random"]:
			return 1, keyword+": Line: " + str(lineno) + ": '" + formode + "' is not a valid for mode."
		
		if isaliteral(start):
			xret=literal_syntax(start, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(end):
			xret=literal_syntax(end, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(step):
			xret=literal_syntax(step, keyword, lineno)
			if xret!=None:
				return xret
		for char in var:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in iteration variable name! '" + char + "'"
		if var in reservednames:
			return 1, keyword+": Line: " + str(lineno) + ": iteration variable name: '" + var + "' Is reserved."

		return 0, None
	def p1(self, args, keyword, lineno):
		var, indummy, formode, modeargs = args.split(" ")
		start, end, step = modeargs.split(",")
		retlist = []
		if isaliteral(start):
			retlist.extend(literal_do(start))
			
		if isaliteral(end):
			retlist.extend(literal_do(end))
		
		if isaliteral(step):
			retlist.extend(literal_do(step))
		retlist.extend([npvar(var, "10x0", vtype=nptype_int)])
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		var, indummy, formode, modeargs = args.split(" ")
		start, end, step = modeargs.split(",")
		for f in [var, start, end, step]:
			if f not in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
		fsyntax_begin(lineno, keyword)
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		var, indummy, formode, modeargs = args.split(" ")
		#moved this to each individual section below, so different for modes
		#can have different argument names & numbers of arguments.
		#start, end, step = modeargs.split(",")
		blockname=fcon_begin(loop=True)
		if formode=="drange":
			start, end, step = modeargs.split(",")
			destobj.write('''#For Loop: Downward range iterator
dataread1;>''' + start + '''
datawrite1;>''' + var + '''
zerosize;;for-drange-loopback-''' +  str(lineno) + '''
goto;>for-drange-subpos-''' +  str(lineno) + '''
zerosize;;''' + fcon_loopback() + '''
dataread1;>''' + var + '''
dataread2;>''' + step + '''
sub
datawrite1;>''' + var + '''
dataread2;>''' + end + '''
gotoifmore;>for-drange-loopback-''' +  str(lineno) + '''
gotoif;>for-drange-loopback-''' +  str(lineno) + '''
goto;>''' + blockname + '''
zerosize;;for-drange-subpos-''' +  str(lineno) + '''
''')
		if formode=="urange":
			start, end, step = modeargs.split(",")
			destobj.write('''#For Loop: Upward range iterator
dataread1;>''' + start + '''
datawrite1;>''' + var + '''
zerosize;;for-drange-loopback-''' +  str(lineno) + '''
goto;>for-drange-subpos-''' +  str(lineno) + '''
zerosize;;''' + fcon_loopback() + '''
dataread1;>''' + var + '''
dataread2;>''' + step + '''
add
datawrite1;>''' + var + '''
dataread2;>''' + end + '''
gotoifless;>for-drange-loopback-''' +  str(lineno) + '''
gotoif;>for-drange-loopback-''' +  str(lineno) + '''
goto;>''' + blockname + '''
zerosize;;for-drange-subpos-''' +  str(lineno) + '''
''')
		#helpful note: `null;;for-random-iter-<lineno>` stores true iteration
		#count! DO NOT REPLACE IT WITH ZEROSIZE!
		if formode=="random":
			start, end, loops = modeargs.split(",")
			destobj.write('''#For Loop: random range iterator
dataread1;>''' + start + '''
iowrite1;>rand1.start
dataread1;>''' + end + '''
iowrite1;>rand1.end
null;;for-random-iter-''' +  str(lineno) + '''
zerosize;;for-random-loopback-''' +  str(lineno) + '''
ioread1;>rand1.get
datawrite1;>''' + var + '''
goto;>for-random-subpos-''' +  str(lineno) + '''
zerosize;;''' + fcon_loopback() + '''
dataread1;>for-random-iter-''' +  str(lineno) + '''
adddata1;10x1
datawrite1;>for-random-iter-''' +  str(lineno) + '''
dataread2;>''' + loops + '''
gotoifless;>for-random-loopback-''' +  str(lineno) + '''
gotoif;>for-random-loopback-''' +  str(lineno) + '''
goto;>''' + blockname + '''
zerosize;;for-random-subpos-''' +  str(lineno) + '''
''')
		return

#same as intcommon1, but supports literals.
class in_intcommon1b:
	def __init__(self, keywords, prearg, postarg, comment):
		self.keywords=keywords
		self.prearg=prearg
		self.postarg=postarg
		self.comment=comment
	def p0(self, args, keyword, lineno):
		if isaliteral(args):
			xret=literal_syntax(args, keyword, lineno)
			if xret!=None:
				return xret
		
		return 0, None
	def p1(self, args, keyword, lineno):
		retlist=[]
		if isaliteral(args):
			retlist.extend(literal_do(args))
			
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		if args in valid_nvars:
			return 0, None
		else:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + self.comment + "\n" + self.prearg + args + self.postarg)
		return



class in_sum:
	def __init__(self):
		self.keywords=["sum"]
		
	def p0(self, args, keyword, lineno):
		for vint in args.split(","):
			if isaliteral(vint):
				xret=literal_syntax(vint, keyword, lineno)
				if xret!=None:
					return xret
		
		return 0, None
	def p1(self, args, keyword, lineno):
		retlist=[]
		for vint in args.split(","):
			if isaliteral(vint):
				retlist.extend(literal_do(vint))
			
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		for vint in args.split(","):
			if vint in valid_nvars:
				pass
			else:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + vint + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#multi-variable SUM \nsetreg1;0\n")
		for vint in args.split(","):
			destobj.write("dataread2;>" + vint + "\nadd\n")
		return


#variable invert (in-place)
#NOTICE: DEPRECIATED
class in_invert:
	def __init__(self):
		self.keywords=["invert"]
		self.comment="invert a variable. WARNING: DEPRECIATED"
		
	def p0(self, args, keyword, lineno):
		print("DEPRECIATION WARNING: 'invert' is depreciated. use 'inv' (with 'set' to store result), instead.")
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		if args in valid_nvars:
			return 0, None
		else:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + self.comment + "\ndataread1;>" + args + "\ninvert1\ndatawrite1;>" + args + "\n")
		return

#table read
class in_tabr:
	def __init__(self):
		self.keywords=["tabr", "tabcd", "tabdd", "tabtd", "tabr2", "tabcd2", "tabdd2", "tabtd2"]
	def p0(self, args, keyword, lineno):
		try:
			tname, xv, yv = args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": Must Specify [name],[xvar],[yvar] as arguments."
		if isaliteral(yv):
			xret=literal_syntax(yv, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(xv):
			xret=literal_syntax(yv, keyword, lineno)
			if xret!=None:
				return xret
			
		
		return 0, None
		
	def p1(self, args, keyword, lineno):
		tname, xv, yv = args.split(",")
		
		retlist=[]
		if isaliteral(xv):
			retlist.extend(literal_do(xv))
		if isaliteral(yv):
			retlist.extend(literal_do(yv))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		
		tname, xv, yv = args.split(",")
		if xv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + xv + "'"
		if yv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + yv + "'"
		if tname not in tables:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant table name '" + tname + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		tname, xv, yv = args.split(",")
		tabvar=tables[tname]
		if keyword.endswith("2"):
			readop="instread1"
		else:
			readop="dataread1"
		destobj.write('''#SSTNPL table read instruction.
dataread1;>''' + yv + '''
muldata1;10x''' + str(tabvar.vdata[0]) + '''
dataread2;>''' + xv + '''
add
adddata1;>''' + tname + '''--table
datawrite1;>tabr--adrbuff--''' + str(lineno) + '''
''' + readop +  ''';;tabr--adrbuff--''' + str(lineno) + '''
''')
		if keyword in ["tabcd", "tabcd2"]:
			destobj.write("iowrite1;>io.ttywr\n")
		if keyword in ["tabdd", "tabdd2"]:
			destobj.write("iowrite1;>io.decdump\n")
		if keyword in ["tabtd", "tabtd2"]:
			destobj.write("iowrite1;>io.tritdump\n")
		return

#table write
class in_tabw:
	def __init__(self):
		self.keywords=["tabw", "tabw2"]
	def p0(self, args, keyword, lineno):
		try:
			tname, xv, yv, datav = args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": Must Specify [name],[xvar],[yvar],[datavar] as arguments."
		if isaliteral(yv):
			xret=literal_syntax(yv, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(xv):
			xret=literal_syntax(yv, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(datav):
			xret=literal_syntax(datav, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		tname, xv, yv, datav = args.split(",")
		retlist=[]
		if isaliteral(xv):
			retlist.extend(literal_do(xv))
		if isaliteral(yv):
			retlist.extend(literal_do(yv))
		if isaliteral(datav):
			retlist.extend(literal_do(datav))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		
		tname, xv, yv, datav = args.split(",")
		if xv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + xv + "'"
		if datav not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + datav + "'"
		if yv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + yv + "'"
		if tname not in tables:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant table name '" + tname + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		tname, xv, yv, datav = args.split(",")
		tabvar=tables[tname]
		if keyword.endswith("2"):
			writeop="instwrite1"
		else:
			writeop="datawrite1"
		destobj.write('''#SSTNPL table write instruction.
dataread1;>''' + yv + '''
muldata1;10x''' + str(tabvar.vdata[0]) + '''
dataread2;>''' + xv + '''
add
adddata1;>''' + tname + '''--table
datawrite1;>tabw--adrbuff--''' + str(lineno) + '''
dataread1;>''' + datav + '''
''' + writeop + ''';;tabw--adrbuff--''' + str(lineno) + '''
''')
		return

#passive character get function.
class in_getchar:
	def __init__(self):
		self.keywords=["getchar"]
		self.comment="Get character from TTY input."
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		if args in valid_nvars:
			return 0, None
		else:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + self.comment + "\nioread1;>io.ttyrd\ndatawrite1;>" + args + "\n")
		return

class in_vdistat:
	def __init__(self):
		self.keywords=["vdistat"]
		self.comment="Get vdi status"
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		if args in valid_nvars:
			return 0, None
		else:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + self.comment + "\nioread1;>vdi.cli.status\ndatawrite1;>" + args + "\n")
		return


#static 3-color & 27-color multi-chunk packart macros
class in_mulpack:
	def __init__(self):
		self.keywords=["mulpk", "linepk", "cmulpk", "clinepk"]
	def p0(self, args, keyword, lineno):
		if args=="":
			return 1, keyword+": Line: " + str(lineno) + ": No data."
		arglist=args.split(";")
		for arg in arglist:
			if len(arg)!=9:
				return 1, keyword+": Line: " + str(lineno) + ": Pack Chunk '" + arg + "' Not 9 trits."
			for char in arg:
				if char not in tritvalid:
					return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Pack Chunk '" + arg + "': '" + char + "'"
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + keyword + "\n")
		if keyword.startswith("c"):
			destobj.write("fopset2;>io.cpack\n")
		arglist=args.split(";")
		for arg in arglist:
			destobj.write("fopwri2;" + arg + "\n")
		if keyword=="linepk" or keyword=="clinepk":
			destobj.write("fopwri1;:\\n\n")
		if keyword.startswith("c"):
			destobj.write("fopset2;>io.packart\n")
		return

#basic goto/gsub implementation.
class in_labelgoto:
	def __init__(self):
		self.keywords=["goto", "gsub"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		if args in labels:
			return 0, None
		else:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + args + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		if keyword=="gsub":
			
			destobj.write("#goto (extra code stores away return address.)\n" + "setreg1;>goto--jumper-" +  str(lineno) + "\ns1push1\ngoto;>" + args +"--label" + "\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		else:
			destobj.write("#goto \n" + "goto;>" + args +"--label" + "\n")
		return

#Conditional operations (WARNING: a bit complicated!)
class in_condgoto:
	def __init__(self, keywords, gotoop, condmode=0, gotoop2=None):
		self.keywords=keywords
		self.gotoop=gotoop
		self.gotoop2=gotoop2
		self.condmode=condmode
	#conditional logic selector function.
	def getcond(self, lineno, var0, var1, thirdarg=None, inverse=False):
		#check wether to inverse flow order. (only used by 'begin' so far.)
		if inverse:
			if self.condmode==0:
				cmode=1
			if self.condmode==1:
				cmode=0
			if self.condmode==2:
				cmode=3
			if self.condmode==3:
				cmode=2
		else:
			cmode=self.condmode
		if cmode==0:
			return '''dataread1;>''' + var0 + '''
dataread2;>''' + var1 + '''
''' + self.gotoop + ''';>goto--branch-''' + str(lineno) + '''
goto;>goto--jumper-''' +  str(lineno)
		if cmode==1:
			return '''dataread1;>''' + var0 + '''
dataread2;>''' + var1 + '''
''' + self.gotoop + ''';>goto--jumper-''' + str(lineno) + '''
goto;>goto--branch-''' +  str(lineno)
		#range checks
		if cmode==2:
			return '''dataread1;>''' + thirdarg + '''
dataread2;>''' + var0 + '''
''' + self.gotoop + ''';>goto--halfstep-''' + str(lineno) + '''
gotoif;>goto--halfstep-''' + str(lineno) + '''
goto;>goto--jumper-''' + str(lineno) + '''
dataread1;>''' + thirdarg + ''';goto--halfstep-''' + str(lineno) + '''
dataread2;>''' + var1 + '''
''' + self.gotoop2 + ''';>goto--branch-''' + str(lineno) + '''
gotoif;>goto--branch-''' + str(lineno) + '''
goto;>goto--jumper-''' + str(lineno)
		#not range
		if cmode==3:
			return '''dataread1;>''' + thirdarg + '''
dataread2;>''' + var0 + '''
''' + self.gotoop + ''';>goto--halfstep-''' + str(lineno) + '''
gotoif;>goto--halfstep-''' + str(lineno) + '''
goto;>goto--branch-''' + str(lineno) + '''
dataread1;>''' + thirdarg + ''';goto--halfstep-''' + str(lineno) + '''
dataread2;>''' + var1 + '''
''' + self.gotoop2 + ''';>goto--jumper-''' + str(lineno) + '''
gotoif;>goto--jumper-''' + str(lineno) + '''
goto;>goto--branch-''' + str(lineno)
	def p0(self, args, keyword, lineno):
		arglist=args.split(" ")
		if len(arglist)!=3:
			if len(arglist)!=2:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify args as '<var>,<var> goto <label>'"
			#return mode doesn't need label argument.
			elif arglist[1] not in ["return", "stop", "break", "begin", "top"]:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify args as '<var>,<var> goto <label>'"
		if self.condmode in [2, 3]:
			try:
				arga, argb, argc=arglist[0].split(",")
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify range condition args as '<startvar>,<endvar>,<valuevar>'"
		else:
			
			try:
				arga, argb=arglist[0].split(",")
				argc=None
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify condition args as '<var>,<var>'"
		###LITERALS
		if isaliteral(arga):
			xret=literal_syntax(arga, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(argb):
			xret=literal_syntax(argb, keyword, lineno)
			if xret!=None:
				return xret
		if argc!=None:
			if isaliteral(argc):
				xret=literal_syntax(argc, keyword, lineno)
				if xret!=None:
					return xret
		if arglist[1] in ["chardump", "dumpt", "dumpd"]:
			if isaliteral(arglist[2]):
				xret=literal_syntax(arglist[2], keyword, lineno)
				if xret!=None:
					return xret
		if arglist[1].startswith("="):
			if isaliteral(arglist[2]):
				xret=literal_syntax(arglist[2], keyword, lineno)
				if xret!=None:
					return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		arglist=args.split(" ")
		if self.condmode in [2, 3]:
			try:
				arga, argb, argc=arglist[0].split(",")
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify range condition args as '<startvar>,<endvar>,<valuevar>'"
		else:
			
			try:
				arga, argb=arglist[0].split(",")
				argc=None
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify condition args as '<var>,<var>'"
		retlist=[]
		if isaliteral(arga):
			retlist.extend(literal_do(arga))
		if isaliteral(argb):
			retlist.extend(literal_do(argb))
		if argc!=None:
			if isaliteral(argc):
				retlist.extend(literal_do(argc))
		if arglist[1].startswith("="):
			if isaliteral(arglist[2]):
				retlist.extend(literal_do(arglist[2]))
		if arglist[1] in ["chardump", "dumpt", "dumpd"]:
			if isaliteral(arglist[2]):
				retlist.extend(literal_do(arglist[2]))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		arglist=args.split(" ")
		#check label for goto and gsub
		if len(arglist)==3 and not arglist[1].startswith("=") and not arglist[1] in ["chardump", "dumpt", "dumpd"]:
			label=arglist[2]
			if not label in labels:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + label + "'"
		if arglist[1].startswith("="):
			vname=arglist[1][1:]
			if vname not in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant destination variable'" + vname + "'"
			valname=arglist[2]
			if valname not in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant source variable'" + vname + "'"
		if arglist[1] in ["chardump", "dumpt", "dumpd"]:
			valname=arglist[2]
			if valname not in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant character variable'" + vname + "'"
		#check goto mode
		if (arglist[1] not in ["begin", "break", "top", "goto", "gsub", "stop", "return", "chardump", "dumpt", "dumpd"]) and (not arglist[1].startswith("=")):
			return 1, keyword+": Line: " + str(lineno) + ": Invalid conditional mode! See documentation for valid modes."
		#variable check
		for x in arglist[0].split(","):
			if not x in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + x + "'"
				
		if arglist[1]=="break":
			retx=fsyntax_break(lineno, keyword)
			if retx!=None:
				return retx
		if arglist[1]=="top":
			retx=fsyntax_top(lineno, keyword)
			if retx!=None:
				return retx
		if arglist[1]=="begin":
			fsyntax_begin(lineno, keyword)
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		arglist=args.split(" ")
		if len(arglist)==3:
			label=arglist[2]
		try:
			var0, var1, thirdarg = arglist[0].split(",")
		except ValueError:
			var0, var1 = arglist[0].split(",")
			thirdarg=None
		#action code for individual 'modes'
		#see getcond for condition logic modes.
		#gsub goto
		if arglist[1]=="gsub":
			destobj.write('''#conditional subroutine goto
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
setreg1;>goto--jumper-''' +  str(lineno) + ";goto--branch-" +  str(lineno) + "\ns1push1\ngoto;>" + label + "--label\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		#set variable
		elif arglist[1].startswith("="):
			destobj.write('''#conditional set
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
dataread1;>''' + arglist[2] + ";goto--branch-" +  str(lineno) + "\ndatawrite1;>" + arglist[1][1:] + "\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		
		#conditional character dump
		elif arglist[1]=="chardump":
			destobj.write('''#conditional chardump
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
dataread1;>''' + arglist[2] + ";goto--branch-" +  str(lineno) + "\niowrite1;>io.ttywr" + "\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		#conditional decimal dump
		elif arglist[1]=="dumpd":
			destobj.write('''#conditional dumpd
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
dataread1;>''' + arglist[2] + ";goto--branch-" +  str(lineno) + "\niowrite1;>io.decdump" + "\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		#conditional ternary dump
		elif arglist[1]=="dumpt":
			destobj.write('''#conditional dumpt
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
dataread1;>''' + arglist[2] + ";goto--branch-" +  str(lineno) + "\niowrite1;>io.tritdump" + "\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		
		
		#return from subroutine
		elif arglist[1]=="return":
			destobj.write('''#conditional return
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
s1pop1;''' + ";goto--branch-" +  str(lineno) + "\ngotoreg1\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		#conditional stop
		elif arglist[1]=="stop":
			destobj.write('''#conditional stop
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
stop;''' + ";goto--branch-" +  str(lineno) + "\n\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		#conditional flow control break
		elif arglist[1]=="break":
			destobj.write('''#conditional flow control break
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
goto;>''' + fcon_break() + ";goto--branch-" +  str(lineno) + "\n\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		elif arglist[1]=="top":
			destobj.write('''#conditional flow control to-top-of-block (top)
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
goto;>''' + fcon_top() + ";goto--branch-" +  str(lineno) + "\n\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		
		#conditional flow control begin
		elif arglist[1]=="begin":
			destobj.write('''#conditional flow control begin
''' + self.getcond(lineno, var0, var1, thirdarg, inverse=True) + '''
goto;>''' + fcon_begin() + ";goto--branch-" +  str(lineno) + "\n\nzerosize;;goto--jumper-" +  str(lineno) + '''
zerosize;;''' + fcon_loopback() + "\n")
		
		#basic goto
		else:
			destobj.write('''#conditional goto
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
setreg1;>goto--jumper-''' +  str(lineno) + ";goto--branch-" +  str(lineno) + "\ngoto;>" + label + "--label\nzerosize;;goto--jumper-" +  str(lineno) + "\n")
		return


#while/until loops
class in_whileuntil:
	def __init__(self, keywords, gotoop, condmode=0, gotoop2=None):
		self.keywords=keywords
		self.gotoop=gotoop
		self.gotoop2=gotoop2
		self.condmode=condmode
	#conditional logic selector function.
	def getcond(self, lineno, var0, var1, thirdarg=None, inverse=False):
		#check wether to inverse flow order. (only used by 'begin' so far.)
		if inverse:
			if self.condmode==0:
				cmode=1
			if self.condmode==1:
				cmode=0
			if self.condmode==2:
				cmode=3
			if self.condmode==3:
				cmode=2
		else:
			cmode=self.condmode
		if cmode==0:
			return '''dataread1;>''' + var0 + '''
dataread2;>''' + var1 + '''
''' + self.gotoop + ''';>goto--branch-''' + str(lineno) + '''
goto;>goto--jumper-''' +  str(lineno)
		if cmode==1:
			return '''dataread1;>''' + var0 + '''
dataread2;>''' + var1 + '''
''' + self.gotoop + ''';>goto--jumper-''' + str(lineno) + '''
goto;>goto--branch-''' +  str(lineno)
		#range checks
		if cmode==2:
			return '''dataread1;>''' + thirdarg + '''
dataread2;>''' + var0 + '''
''' + self.gotoop + ''';>goto--halfstep-''' + str(lineno) + '''
gotoif;>goto--halfstep-''' + str(lineno) + '''
goto;>goto--jumper-''' + str(lineno) + '''
dataread1;>''' + thirdarg + ''';goto--halfstep-''' + str(lineno) + '''
dataread2;>''' + var1 + '''
''' + self.gotoop2 + ''';>goto--branch-''' + str(lineno) + '''
gotoif;>goto--branch-''' + str(lineno) + '''
goto;>goto--jumper-''' + str(lineno)
		#not range
		if cmode==3:
			return '''dataread1;>''' + thirdarg + '''
dataread2;>''' + var0 + '''
''' + self.gotoop + ''';>goto--halfstep-''' + str(lineno) + '''
gotoif;>goto--halfstep-''' + str(lineno) + '''
goto;>goto--branch-''' + str(lineno) + '''
dataread1;>''' + thirdarg + ''';goto--halfstep-''' + str(lineno) + '''
dataread2;>''' + var1 + '''
''' + self.gotoop2 + ''';>goto--jumper-''' + str(lineno) + '''
gotoif;>goto--jumper-''' + str(lineno) + '''
goto;>goto--branch-''' + str(lineno)
	def p0(self, args, keyword, lineno):
		if self.condmode in [2, 3]:
			try:
				arga, argb, argc=args.split(",")
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify range condition args as '<startvar>,<endvar>,<valuevar>'"
		else:
			
			try:
				arga, argb=args.split(",")
				argc=None
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify condition args as '<var>,<var>'"
		###LITERALS
		if isaliteral(arga):
			xret=literal_syntax(arga, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(argb):
			xret=literal_syntax(argb, keyword, lineno)
			if xret!=None:
				return xret
		if argc!=None:
			if isaliteral(argc):
				xret=literal_syntax(argc, keyword, lineno)
				if xret!=None:
					return xret
		
		return 0, None
	def p1(self, args, keyword, lineno):
		if self.condmode in [2, 3]:
			try:
				arga, argb, argc=args.split(",")
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify range condition args as '<startvar>,<endvar>,<valuevar>'"
		else:
			
			try:
				arga, argb=args.split(",")
				argc=None
			except ValueError:
				return 1, keyword+": Line: " + str(lineno) + ": Must specify condition args as '<var>,<var>'"
		retlist=[]
		if isaliteral(arga):
			retlist.extend(literal_do(arga))
		if isaliteral(argb):
			retlist.extend(literal_do(argb))
		if argc!=None:
			if isaliteral(argc):
				retlist.extend(literal_do(argc))
		
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		#variable check
		for x in args.split(","):
			if not x in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + x + "'"
		fsyntax_begin(lineno, keyword)
		return 0, None
		

	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		try:
			var0, var1, thirdarg = args.split(",")
		except ValueError:
			var0, var1 = args.split(",")
			thirdarg=None
		#action code for individual 'modes'
		#see getcond for condition logic modes.
		#gsub goto
		blockname=fcon_begin(loop=True)
		destobj.write('''#conditional flow control begin
null;;''' + fcon_loopback() + '''
''' + self.getcond(lineno, var0, var1, thirdarg, inverse=True) + '''
goto;>''' + blockname + ";goto--branch-" +  str(lineno) + '''
zerosize;;goto--jumper-''' +  str(lineno) + "\n")
		return

#common 2-operator math class
class in_int2opmath:
	def __init__(self, keywords, instruct, comment):
		self.keywords=keywords
		self.instruct=instruct
		self.comment=comment
	def p0(self, args, keyword, lineno):
		argsplit=args.split(",")
		if len(argsplit)!=2:
			return 1, keyword+": Line: " + str(lineno) + ": Two comma-separated variable/literal arguments required!"
		arga, argb=args.split(",")
		if isaliteral(arga):
			xret=literal_syntax(arga, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(argb):
			xret=literal_syntax(argb, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		arga, argb=args.split(",")
		retlist=[]
		if isaliteral(arga):
			retlist.extend(literal_do(arga))
		if isaliteral(argb):
			retlist.extend(literal_do(argb))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		argsplit=args.split(",")
		for argx in argsplit:
			if argx in valid_nvars:
				return 0, None
			else:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + argx + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		arg0, arg1 = args.split(",")
		destobj.write("#" + self.comment + "\ndataread1;>" + arg0 + "\ndataread2;>" + arg1 + "\n" + self.instruct)
		return



#random number implementation based upon SBTCVM psudo-random number generator 'rand1'.
class in_rrange:
	def __init__(self):
		self.keywords=["rrange"]
		self.comment="Random ranged number"
	def p0(self, args, keyword, lineno):
		argsplit=args.split(",")
		if len(argsplit)!=2:
			return 1, keyword+": Line: " + str(lineno) + ": Two comma-separated variable arguments required!"
		arga, argb=args.split(",")
		
		if isaliteral(arga):
			xret=literal_syntax(arga, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(argb):
			xret=literal_syntax(argb, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		arga, argb=args.split(",")
		retlist=[]
		if isaliteral(arga):
			retlist.extend(literal_do(arga))
		if isaliteral(argb):
			retlist.extend(literal_do(argb))
		
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		argsplit=args.split(",")
		for argx in argsplit:
			if argx in valid_nvars:
				return 0, None
			else:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + argx + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		arg0, arg1 = args.split(",")
		destobj.write("#" + self.comment + "\ndataread1;>" + arg0 + "\ndataread2;>" + arg1 + "\niowrite1;>rand1.start\n" + "iowrite2;>rand1.end\n" + "ioread1;>rand1.get")
		return

#variable swap
class in_int2opswap:
	def __init__(self):
		self.keywords=["swap"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		argsplit=args.split(",")
		if len(argsplit)!=2:
			return 1, keyword+": Line: " + str(lineno) + ": Two comma-separated variable arguments required!"
		for argx in argsplit:
			if argx in valid_nvars:
				return 0, None
			else:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + argx + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		arg0, arg1 = args.split(",")
		destobj.write("#swap variables \ndataread1;>" + arg0 + "\ndataread2;>" + arg1 + "\ndatawrite1;>" + arg1 + "\ndatawrite2;>" + arg0 + "\n")
		return
	

#variable copy
class in_int2opcopy:
	def __init__(self):
		self.keywords=["copy"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		argsplit=args.split(",")
		if len(argsplit)!=2:
			return 1, keyword+": Line: " + str(lineno) + ": Two comma-separated variable arguments required!"
		for argx in argsplit:
			if argx in valid_nvars:
				return 0, None
			else:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + argx + "'"
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		arg0, arg1 = args.split(",")
		destobj.write("#copy variables \ndataread1;>" + arg0 + "\ndatawrite1;>" + arg1 + "\n")
		return

#common no-argument command class
class in_common0:
	def __init__(self, keywords, xcode, comment):
		self.keywords=keywords
		self.xcode=xcode
		self.comment=comment
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + self.comment + "\n" + self.xcode)
		return
		

#Active equivalent to getchar. will only continue on a non-null character from TTY.
class in_keyprompt:
	def __init__(self):
		self.keywords=["keyprompt"]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#keprompt: prompt for single keypress, continue only when keypress is received." + """
setreg2;0
iowrite1;>io.ttyrd
ioread1;>io.ttyrd;keyprompt--loop-""" + str(lineno) + """
gotoif;>keyprompt--loop-""" + str(lineno) + """
""")
		return
		

#upwards 2-axis iterator
class in_u2iter:
	def __init__(self):
		self.keywords=["u2iter"]
	def p0(self, args, keyword, lineno):
		try:
			namex, namey, subx, startx, endx, starty, endy = args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid argument sequence.'" + char + "'"
		for char in namex:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Iterator X State Integer variable! '" + char + "'"
		for char in namey:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Iterator Y State Integer variable! '" + char + "'"

		if isaliteral(startx):
			xret=literal_syntax(startx, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(endx):
			xret=literal_syntax(endx, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(starty):
			xret=literal_syntax(starty, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(endy):
			xret=literal_syntax(endy, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		namex, namey, subx, startx, endx, starty, endy = args.split(",")
		retlist=[]
		retlist.extend([npvar(namex, "10x0", vtype=nptype_int)])
		retlist.extend([npvar(namey, "10x0", vtype=nptype_int)])
		if isaliteral(startx):
			retlist.extend(literal_do(startx))
		if isaliteral(endx):
			retlist.extend(literal_do(endx))
		if isaliteral(starty):
			retlist.extend(literal_do(starty))
		if isaliteral(endy):
			retlist.extend(literal_do(endy))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		namex, namey, subx, startx, endx, starty, endy = args.split(",")
		if subx not in labels:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + subx + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		namex, namey, subx, startx, endx, starty, endy = args.split(",")
		destobj.write('''#XY Upward range iterator
dataread1;>''' + starty + '''
datawrite1;>''' + namey + '''
dataread1;>''' + startx + ''';u2iter-yloop-''' +  str(lineno) + '''
datawrite1;>''' + namex + '''
setreg1;>u2iter-retpos-''' +  str(lineno) + ''';u2iter-loopback-''' +  str(lineno) + '''
s1push1
goto;>''' + subx + '''--label
dataread1;>''' + namex + ''';u2iter-retpos-''' +  str(lineno) + '''
setreg2;10x1
add
datawrite1;>''' + namex + '''
dataread2;>''' + endx + '''
gotoifless;>u2iter-loopback-''' +  str(lineno) + '''
gotoif;>u2iter-loopback-''' +  str(lineno) + '''
dataread1;>''' + namey + '''
setreg2;10x1
add
datawrite1;>''' + namey + '''
dataread2;>''' + endy + '''
gotoifless;>u2iter-yloop-''' +  str(lineno) + '''
gotoif;>u2iter-yloop-''' +  str(lineno) + '''
''')
		return
#downwards 2-axis iterator
class in_d2iter:
	def __init__(self):
		self.keywords=["d2iter"]
	def p0(self, args, keyword, lineno):
		try:
			namex, namey, subx, startx, endx, starty, endy = args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid argument sequence.'" + char + "'"
		for char in namex:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Iterator X State Integer variable! '" + char + "'"
		for char in namey:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Iterator Y State Integer variable! '" + char + "'"

		if isaliteral(startx):
			xret=literal_syntax(startx, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(endx):
			xret=literal_syntax(endx, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(starty):
			xret=literal_syntax(starty, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(endy):
			xret=literal_syntax(endy, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		namex, namey, subx, startx, endx, starty, endy = args.split(",")
		retlist=[]
		retlist.extend([npvar(namex, "10x0", vtype=nptype_int)])
		retlist.extend([npvar(namey, "10x0", vtype=nptype_int)])
		if isaliteral(startx):
			retlist.extend(literal_do(startx))
		if isaliteral(endx):
			retlist.extend(literal_do(endx))
		if isaliteral(starty):
			retlist.extend(literal_do(starty))
		if isaliteral(endy):
			retlist.extend(literal_do(endy))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		namex, namey, subx, startx, endx, starty, endy = args.split(",")
		if subx not in labels:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + subx + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		namex, namey, subx, startx, endx, starty, endy = args.split(",")
		destobj.write('''#XY Downward range iterator
dataread1;>''' + starty + '''
datawrite1;>''' + namey + '''
dataread1;>''' + startx + ''';d2iter-yloop-''' +  str(lineno) + '''
datawrite1;>''' + namex + '''
setreg1;>d2iter-retpos-''' +  str(lineno) + ''';d2iter-loopback-''' +  str(lineno) + '''
s1push1
goto;>''' + subx + '''--label
dataread1;>''' + namex + ''';d2iter-retpos-''' +  str(lineno) + '''
setreg2;10x1
sub
datawrite1;>''' + namex + '''
dataread2;>''' + endx + '''
gotoifmore;>d2iter-loopback-''' +  str(lineno) + '''
gotoif;>d2iter-loopback-''' +  str(lineno) + '''
dataread1;>''' + namey + '''
setreg2;10x1
sub
datawrite1;>''' + namey + '''
dataread2;>''' + endy + '''
gotoifmore;>d2iter-yloop-''' +  str(lineno) + '''
gotoif;>d2iter-yloop-''' +  str(lineno) + '''
''')
		return



#upwards 1-axis iterator
class in_uiter:
	def __init__(self):
		self.keywords=["uiter"]
	def p0(self, args, keyword, lineno):
		try:
			namex, subx, startx, endx = args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid argument sequence.'" + char + "'"
		for char in namex:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Iterator State Integer variable! '" + char + "'"
		if isaliteral(startx):
			xret=literal_syntax(startx, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(endx):
			xret=literal_syntax(endx, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		namex, subx, startx, endx = args.split(",")
		retlist=[]
		retlist.extend([npvar(namex, "10x0", vtype=nptype_int)])
		if isaliteral(startx):
			retlist.extend(literal_do(startx))
		if isaliteral(endx):
			retlist.extend(literal_do(endx))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		namex, subx, startx, endx = args.split(",")
		
		if subx not in labels:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + subx + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		namex, subx, startx, endx = args.split(",")
		destobj.write('''#Upward range iterator
dataread1;>''' + startx + '''
datawrite1;>''' + namex + '''
setreg1;>uiter-retpos-''' +  str(lineno) + ''';uiter-loopback-''' +  str(lineno) + '''
s1push1
goto;>''' + subx + '''--label
dataread1;>''' + namex + ''';uiter-retpos-''' +  str(lineno) + '''
setreg2;10x1
add
datawrite1;>''' + namex + '''
dataread2;>''' + endx + '''
gotoifless;>uiter-loopback-''' +  str(lineno) + '''
gotoif;>uiter-loopback-''' +  str(lineno) + '''

''')
		return


# basic cycle-based 'sleep-like' instruction.
class in_waitcycle:
	def __init__(self):
		self.keywords=["waitcy"]
	def p0(self, args, keyword, lineno):
		try:
			argint=int(args)
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid cycle count integer'" + args + "'"
		#value can't be any lower than 6, as the loop wouldn't run at all.
		if argint<6:
			return 1, keyword+": Line: " + str(lineno) + ": '" + args + "' is less than the minimum supported cycle count (6)"
		
		#ensure value is at or below 9841 once divided by wait loop length (6) aka 59046
		if argint>59046:
			return 1, keyword+": Line: " + str(lineno) + ": '" + args + "' is greater than the maximum supported cycle count (59046)"
		
		if argint % 6 != 0:
			print("SUM: Notice: the requested wait time: '" + args + "' is not divisible by 6. \n      Actual wait time: '" + str((argint//6)*6) + "'")
		
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		argint=int(args)//6
		destobj.write('''#Wait loop
setreg1;0
datawrite1;>waitcy-loopback-''' +  str(lineno) + '''
setreg1;0;waitcy-loopback-''' +  str(lineno) + '''
setreg2;10x1
add
datawrite1;>waitcy-loopback-''' +  str(lineno) + '''
setreg2;10x''' + str(argint) + '''
gotoifless;>waitcy-loopback-''' +  str(lineno) + '''

''')
		return
#downwards 1-axis iterator
class in_diter:
	def __init__(self):
		self.keywords=["diter"]
	def p0(self, args, keyword, lineno):
		try:
			namex, subx, startx, endx = args.split(",")
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid argument sequence.'" + char + "'"
		for char in namex:
			if char not in varvalid:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid character in Iterator State Integer variable! '" + char + "'"
		if isaliteral(startx):
			xret=literal_syntax(startx, keyword, lineno)
			if xret!=None:
				return xret
		if isaliteral(endx):
			xret=literal_syntax(endx, keyword, lineno)
			if xret!=None:
				return xret
		return 0, None
	def p1(self, args, keyword, lineno):
		namex, subx, startx, endx = args.split(",")
		retlist=[]
		if isaliteral(startx):
			retlist.extend(literal_do(startx))
		if isaliteral(endx):
			retlist.extend(literal_do(endx))
		retlist.extend([npvar(namex, "10x0", vtype=nptype_int)])
		
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		namex, subx, startx, endx = args.split(",")
		
		if subx not in labels:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + subx + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		namex, subx, startx, endx = args.split(",")
		destobj.write('''#Downward range iterator
dataread1;>''' + startx + '''
datawrite1;>''' + namex + '''
setreg1;>diter-retpos-''' +  str(lineno) + ''';diter-loopback-''' +  str(lineno) + '''
s1push1
goto;>''' + subx + '''--label
dataread1;>''' + namex + ''';diter-retpos-''' +  str(lineno) + '''
setreg2;10x1
sub
datawrite1;>''' + namex + '''
dataread2;>''' + endx + '''
gotoifmore;>diter-loopback-''' +  str(lineno) + '''
gotoif;>diter-loopback-''' +  str(lineno) + '''

''')
		return




#print/prline statement.
#also handles table string tstr syntax
class in_print:
	def __init__(self):
		self.keywords=["print", "prline", "tstr", "vdi", "vdin"]
		self.comment="print"
	def p0(self, args, keyword, lineno):
		for char in args:
			if char not in tcon.normal_char_list:
				return 1, keyword+": Line: " + str(lineno) + ": invalid character'" + char + "'"
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + keyword + "\n")
		if keyword=="vdi" or keyword=="vdin":
			destobj.write("fopset1;>vdi.cli.in\n")
			
		for char in args:
			if keyword=="tstr":
				destobj.write("null;:" + tcon.chartoasmchar[char] + "\n")
			else:
				destobj.write("fopwri1;:" + tcon.chartoasmchar[char] + "\n")
		if keyword=="prline" or keyword=="vdi":
			destobj.write("fopwri1;:\\n\n")
		if keyword=="vdi" or keyword=="vdin":
			destobj.write("fopset1;>io.ttywr\n")
		return

#used by 
class in_str_out:
	def __init__(self, keywords, ioaddr, newl=1):
		self.keywords=keywords
		self.newl=newl
		self.io=ioaddr
	def p0(self, args, keyword, lineno):
		for char in args:
			if char not in tcon.normal_char_list:
				return 1, keyword+": Line: " + str(lineno) + ": invalid character'" + char + "'"
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + keyword + "\n")
		destobj.write("fopset1;" + self.io + "\n")
		
		for char in args:
			destobj.write("fopwri1;:" + tcon.chartoasmchar[char] + "\n")
		if self.newl:
			destobj.write("fopwri1;:\\n\n")
		destobj.write("fopset1;>io.ttywr\n")
		return

class in_tpad:
	def __init__(self):
		self.keywords=["tpad"]
		self.comment="Table Pad (tpad)"
	def p0(self, args, keyword, lineno):
		try:
			intarg=int(args)
			if intarg<1:
				return 1, keyword+": Line: " + str(lineno) + ": tpad size must be 1 or higher!" + arg + "'"
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": invalid tpad size integer'" + arg + "'"
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + keyword + "\n")
		intarg=int(args)
		#try python2 xrange, assume python 3 if NameError
		try:
			for f in xrange(0, intarg):
				destobj.write("null;0\n")
		except NameError:
			for f in range(0, intarg):
				destobj.write("null;0\n")
		return

class in_tabstrc:
	def __init__(self):
		self.keywords=["tabstrc"]
		self.comment="table string check (for command checking.)"
	def p0(self, args, keyword, lineno):
		arglist=args.split(",")
		if len(arglist)!=4:
			return 1, keyword+": Line: " + str(lineno) + ": Please specify arguments as: '[table],[xoffset],[ypos],[string]'"
		xoffset=arglist[1]
		if isaliteral(xoffset):
			xret=literal_syntax(xoffset, keyword, lineno)
			if xret!=None:
				return xret
		ypos=arglist[2]
		if isaliteral(ypos):
			xret=literal_syntax(ypos, keyword, lineno)
			if xret!=None:
				return xret
		if len(arglist[3])==0:
			return 1, keyword+": Line: " + str(lineno) + ": string must not be zerosize!"

		return 0, None
	def p1(self, args, keyword, lineno):
		arglist=args.split(",")
		xoffset=arglist[1]
		ypos=arglist[2]
		retlist=[]
		if isaliteral(xoffset):
			retlist.extend(literal_do(xoffset))
		if isaliteral(ypos):
			retlist.extend(literal_do(ypos))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		arglist=args.split(",")
		xoffset=arglist[1]
		ypos=arglist[2]
		tname=arglist[0]
		if xoffset not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + xoffset + "'"
		if ypos not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + ypos + "'"
		if tname not in tables:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant table name '" + tname + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#######" + keyword + "\n")
		arglist=args.split(",")
		xoffset=arglist[1]
		ypos=arglist[2]
		tname=arglist[0]
		tabvar=tables[tname]
		stringx=arglist[3]
		stringlist=[]
		for x in stringx:
			stringlist.append(x)
		destobj.write('''#init
setreg1;10x''' + str(tabvar.vdata[0]) + '''
dataread2;>''' + ypos + '''
mul
dataread2;>''' + xoffset + '''
add
adddata1;>''' + tname + '''--table
datawrite1;>tabstrc--adrbuff--''' + str(lineno) + '''
null;;tabstrc--adrbuff--''' + str(lineno) + '''
#reset output buffer to 0
setreg1;0
datawrite1;>tabstrc--outbuff--''' + str(lineno) + '''
null;;tabstrc--outbuff--''' + str(lineno) + '''
#recursive_parser
''')
		#recursive_parser
		counter=0
		self.recursive_parse(stringlist, counter, lineno, destobj, first=1)
		
		destobj.write('''#read output to register 1 for 'set' to use.
dataread1;>tabstrc--outbuff--''' + str(lineno) + '''
''')
		destobj.write("#######" + keyword + " END\n")
		return
	def recursive_parse(self, slist, counter, lineno, destobj, first=0):
		
		counter+=1
		char=slist.pop(0)
		#print("Recursion: " + str(char) + " " + str(counter))
		destobj.write('''#recursion
''')
####### If not first level, increment pointer.
		if not first:
			destobj.write('''#increment pointer
dataread1;>tabstrc--adrbuff--''' + str(lineno) + '''
adddata1;+
datawrite1;>tabstrc--adrbuff--''' + str(lineno) + '''
''')

########Read value from table, run checks
		destobj.write('''
setreg1;>tabstrc--adrbuff--''' + str(lineno) + '''

datawrite1;>tabstrc--recurs-tabbuff--''' + str(lineno) + '_' + str(counter) + '''
dataread1;;tabstrc--recurs-tabbuff--''' + str(lineno) + '_' + str(counter) + '''
datawrite1;>tabstrc--recurs-tabbuff_read--''' + str(lineno) + '_' + str(counter) + '''
dataread1;;tabstrc--recurs-tabbuff_read--''' + str(lineno) + '_' + str(counter) + '''

setreg2;:''' + char + '''


gotoif;>tabstrc--recurs-checkyes--''' + str(lineno) + '_' + str(counter) + '''
goto;>tabstrc--recurs-checkno--''' + str(lineno) + '_' + str(counter) + '''
zerosize;;tabstrc--recurs-checkyes--''' + str(lineno) + '_' + str(counter) + '''
''')
#######If list is now empty, set flag
		if slist==[]:
			destobj.write('''##set flag########
setreg1;>tabstrc--outbuff--''' + str(lineno) + '''
datawrite1;>tabstrc--recurs-flag--''' + str(lineno) + "_" + str(counter) + '''
setreg1;+
datawrite1;;tabstrc--recurs-flag--''' + str(lineno) + "_" + str(counter) + '''
''')
#######if list isn't empty, keep recursively parsing.
		else:
			self.recursive_parse(slist, counter, lineno, destobj)
####### SKip recursion endpoint
		destobj.write('''#recursionskip endpoint
zerosize;;tabstrc--recurs-checkno--''' + str(lineno) + '_' + str(counter) + '''
''')
		return
		

#generic data table syntax
class in_tdat:
	def __init__(self):
		self.keywords=["tdat"]
	def p0(self, args, keyword, lineno):
		if args=="":
			return 1, keyword+": Line: " + str(lineno) + ": Blank table Error"
		arglist=args.split(";")
		for arg in arglist:
			sublist=arg.split(" ")
			if len(sublist)>2:
				return 1, keyword+": Line: " + str(lineno) + ": Invalid double.  '" + arg + "' please use format: 'arg1a arg1b;arg2a arg2b' etc."
			for subarg in sublist:
				if subarg.replace("@", "10x").startswith("10x"):
					try:
						int(subarg.replace("@", "10x")[3:])
					except ValueError:
						return 1, keyword+": Line: " + str(lineno) + ": decimal int syntax error!: '" + subarg + "' "
				elif subarg.startswith(":"):
					if len(subarg)<2:
						return 1, keyword+": Line: " + str(lineno) + ": Must specify character: '" + subarg + "' "
				else:
					if len(subarg.replace("*", ""))>9:
						return 1, keyword+": Line: " + str(lineno) + ": string too lsubarge!: '" + subarg + "' "
					for char in subarg.replace("*", ""):
						
						if char not in tritvalid:
							return 1, keyword+": Line: " + str(lineno) + ": invalid char in ternary data string!: '" + subarg + "' "
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#" + keyword + "\n")
		arglist=args.split(";")
		
		for arg in arglist:
			try:
				suba, subb=arg.split(" ")
				if suba.startswith("@"):
					suba=suba.replace("@", "10x")
				if suba.startswith("*"):
					suba=suba.replace("*", "")
				if subb.startswith("@"):
					subb=subb.replace("@", "10x")
				if subb.startswith("*"):
					subb=subb.replace("*", "")
				destobj.write("raw;" + suba + "," + subb + "\n")
			except ValueError:
				
				if arg.startswith("@"):
					arg=arg.replace("@", "10x")
				if arg.startswith("*"):
					arg=arg.replace("*", "")
				destobj.write("null;" + arg + "\n")
		
		return
# literal syntax detection. (used by literal-supporting command classes to
# detect wether an integer variable name is actually a literal.)
def isaliteral(arg):
	if arg.startswith("@"):
		return 1
	if arg.startswith(":"):
		return 1
	if arg.startswith("*"):
		return 1
	if arg.startswith("$"):
		return 1
	return 0

#literal syntax checker. (literal-supporting command classes call this to check
#syntax of literals.
def literal_syntax(arg, keyword, lineno):
	if arg.startswith("$"):
		if arg[1:] not in constants:
			print(constants)
			return 1, keyword+": Line: " + str(lineno) + ": constant: '" + arg + "' not valid builtin/declared constant"
	if arg.startswith("@"):
		try:
			int(arg[1:])
		except ValueError:
			return 1, keyword+": Line: " + str(lineno) + ": Invalid static integer value '" + arg + "' Must use signed decimal."
	if arg.startswith(":"):
		if arg[1:] not in tcon.asm_chrtodat:
			return 1, keyword+": Line: " + str(lineno) + ": invalid character in literal'" + arg + "'"
	if arg.startswith("*"):
		for x in arg[1:]:
			if x not in tritvalid:
				return 1, keyword+": Line: " + str(lineno) + ": invalid ternary literal'" + arg + "'"
	return None
	
#literal syntax parser engine.(used by literal-supporting command classes to
#  parse literals into variable instances. (variable objects are returned to
#  mainloop by the command classes.)
def literal_do(arg):
	if arg.startswith("@"):
		return [npvar(arg, "10x" + arg[1:], vtype=nptype_int)]
	if arg.startswith(":"):
		return [npvar(arg, ":" + arg[1:], vtype=nptype_int)]
	if arg.startswith("*"):
		return [npvar(arg, arg[1:], vtype=nptype_int)]
	if arg.startswith("$"):
		return [npvar(arg, constants[arg[1:]], vtype=nptype_int)]
		

#header generator.
def headinfo(filename, basename):
	return '''#SSTNPL COMPILER ''' + stnpvers + '''
#header
head-rname=''' + basename + '''
head-nspin=stdnsp
fopset1;>io.ttywr
fopset2;>io.packart
#stnp source file: (autogenerated from) "''' + filename + '''
'''

#main compiler routine.
def compwrap(sourcepath):
	##SSTNPL compile procedure function.
	
	basepath=sourcepath.rsplit(".", 1)[0]
	bpdir=os.path.dirname(basepath)
	bpname=os.path.basename(basepath)
	asmname=bpname
	
	#open source file and init mainloop class
	if asmname.startswith("auto_"):
		asmname="x_" + asmname
	destpath=os.path.join(bpdir, asmname + "__stnp.tasm")
	sourcefile=open(sourcepath, 'r')
	print("SSTNPL: MAIN COMPILER STARTUP:")
	mainl=mainloop(sourcefile, destpath, sourcepath, bpname)
	print("Pass MD: preparse macro definitions")
	mainret=mainl.p_macrodef()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass B: preparse split lines")
	mainret=mainl.p_preparser()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass V: Parser Validation")
	mainret=mainl.p_parsevalid()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass C: constants syntax check")
	mainret=mainl.p_const()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass 0: first syntax check")
	mainret=mainl.p0()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass 1: variable pass")
	mainl.p1()
	print("Pass 2: second syntax check (with variables)")
	mainret=mainl.p2()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass 3: compile pass")
	mainl.p3()
	print("autorunning assembler:")
	#call(['python',  'g2asm.py', destpath])
	#call assembler's wrapper function.
	g2asmlib.assemble(destpath, syntaxonly=0, pfx=("g2asm:   "))
	return

#module compiler routine
def modcomp(sourcepath):
	##SSTNPL compile procedure function.
	
	basepath=sourcepath.rsplit(".", 1)[0]
	bpdir=os.path.dirname(basepath)
	bpname=os.path.basename(basepath)
	asmname=bpname
	
	#open source file and init mainloop class
	#if asmname.startswith("auto_"):
	#	asmname="x_" + asmname
	destpath=os.path.join(bpdir, asmname + ".tas0")
	mfspath=os.path.join(bpdir, asmname + ".stnpmfs")
	
	sourcefile=open(sourcepath, 'r')
	print("SSTNPL: MODULE COMPILER STARTUP:")
	mainl=mainloop(sourcefile, destpath, sourcepath, bpname)
	print("Pass MD: preparse macro definitions")
	mainret=mainl.p_macrodef()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass B: preparse split lines")
	mainret=mainl.p_preparser()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass V: Parser Validation")
	mainret=mainl.p_parsevalid()
	if mainret[0]==1:
		sys.exit(mainret[1])
	
	print("Pass C: constants syntax check")
	mainret=mainl.p_const()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass 0: first syntax check")
	mainret=mainl.p0()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass 1: variable pass")
	mainl.p1()
	print("Pass 2: second syntax check (with variables)")
	mainret=mainl.p2()
	if mainret[0]==1:
		sys.exit(mainret[1])
	print("Pass 3: compile pass")
	mainl.p3()
	print("Pass 4: Generate SSTNPL variable Manifest...")
	mainl.mfs(mfspath)
	return


def DO_buffer(num):
	return [in_common0(["brdhead" + num], "ioread1;>buffer." + num + ".read.head\n", "buffer " + num + " head read"),
	in_common0(["brdtail" + num], "ioread1;>buffer." + num + ".read.tail\n", "buffer " + num + " tail read"),
	in_common0(["breset" + num], "iowrite1;>buffer." + num + ".reset\n", "buffer " + num + " reset"),
	in_intcommon1b(["bwrhead" + num], "dataread1;>", "\niowrite1;>buffer." + num + ".write.head\n", "buffer " + num + " head write"),
	in_intcommon1b(["bwrtail" + num], "dataread1;>", "\niowrite1;>buffer." + num + ".write.tail\n", "buffer " + num + " tail write"),
	in_str_out(["bprinthead" + num], ">buffer." + num + ".write.head", newl=True),
	in_str_out(["bprinttail" + num], ">buffer." + num + ".write.tail", newl=True),
	in_str_out(["bprinthead" + num + "n"], ">buffer." + num + ".write.head", newl=False),
	in_str_out(["bprinttail" + num + "n"], ">buffer." + num + ".write.tail", newl=False)]

class in_macro_def:
	def __init__(self):
		self.keywords=["def"]
	def pmacro(self, args, keyword, lineno):
		try:
			name, code = args.split(" ", 1)
			for f in name:
				if f not in varvalid:
					return 1, "def: (line " + str(lineno) + "): invalid character '" + f + "' in macro name '" + name + "'"
		except ValueError:
			return 1, "def: Syntax Error! must use form 'def name code'"
		return [npvar(name, code, vtype=nptype_macro)]
	def p0(self, args, keyword, lineno):
		return 0, None
	def p1(self, args, keyword, lineno):
		return []
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		return

def macroarg_count(macro_code):
	argcnt=0
	incode=True
	while incode:
		key="%" + str(argcnt) + "%"
		if key in macro_code:
			argcnt+=1
		else:
			incode=False
	return argcnt
	
	
#SSTNPL Compiler Engine class.
class mainloop:
	def __init__(self, srcobj, destpath, sourcepath, bpname):
		self.filename=sourcepath
		self.srcobj=srcobj
		self.outobj=open(destpath, "w")
		self.destpath=destpath
		self.nvars=[]
		self.valid_nvars=[]
		self.tables={}
		self.localconstants=[]
		self.comped_nvars=[]
		##############################
		#master instruction list
		self.instructs=[in_var(),
		in_macro_def(),
		in_include(),
		in_label(),
		in_table(),
		in_tabr(),
		in_tabw(),
		in_tdat(),
		in_tpad(),
		in_tabstrc(),
		in_uiter(),
		in_diter(),
		in_u2iter(),
		in_d2iter(),
		in_sum(),
		in_waitcycle(),
		in_intcommon1b(["dumpt"], "dataread1;>", "\niowrite1;>io.tritdump\n", "Dump (trits)"),
		in_intcommon1b(["vdimode"], "dataread1;>", "\niowrite1;>vdi.cli.status\n", "vdi mode set"),
		in_intcommon1b(["abs"], "dataread1;>", "\nabs1\n", "Get abs of var"),
		in_intcommon1b(["inv"], "dataread1;>", "\ninvert1\n", "Get signwise/tritwise inversion of var"),
		in_intcommon1b(["nabs"], "dataread1;>", "\nnabs1\n", "Get inverted abs of var"),
		in_intcommon1b(["chardump"], "dataread1;>", "\niowrite1;>io.ttywr\n", "Dump (character)"),
		in_intcommon1b(["textcolor"], "dataread1;>", "\niowrite1;>io.textcolor\n", "Set text colors"),
		in_intcommon1b(["packcolor"], "dataread1;>", "\niowrite1;>io.packcolor\n", "Set ternary packed art colors"),
		in_intcommon1b(["tpack"], "dataread1;>", "\niowrite1;>io.packart\n", "Draw ternary Packed art"),
		in_intcommon1b(["cpack"], "dataread1;>", "\niowrite1;>io.cpack\n", "Draw COLOR ternary Packed art"),
		in_mulpack(),
		in_intcommon1b(["gamode"], "dataread1;>", "\niowrite1;>ga.mode\n", "Set SBTGA mode"),
		in_intcommon1b(["drawx1"], "dataread1;>", "\niowrite1;>plot.x1\n", "plotter x pos 1"),
		in_intcommon1b(["drawy1"], "dataread1;>", "\niowrite1;>plot.y1\n", "plotter y pos 1"),
		in_intcommon1b(["drawx2"], "dataread1;>", "\niowrite1;>plot.x2\n", "plotter x pos 2"),
		in_intcommon1b(["drawy2"], "dataread1;>", "\niowrite1;>plot.y2\n", "plotter y pos 2"),
		in_intcommon1b(["drawx3"], "dataread1;>", "\niowrite1;>plot.x3\n", "plotter x pos 3"),
		in_intcommon1b(["drawy3"], "dataread1;>", "\niowrite1;>plot.y3\n", "plotter y pos 3"),
		in_intcommon1b(["drawcopy"], "dataread1;>", "\niowrite1;>plot.copy\n", "plotter buffer copy"),
		in_intcommon1b(["drawblit"], "dataread1;>", "\niowrite1;>plot.blit\n", "plotter buffer blit"),
		in_intcommon1b(["drawselect"], "dataread1;>", "\niowrite1;>plot.select\n", "plotter buffer select"),
		in_intcommon1b(["drawwidth"], "dataread1;>", "\niowrite1;>plot.width\n", "plotter width"),
		in_intcommon1b(["drawheight"], "dataread1;>", "\niowrite1;>plot.height\n", "plotter height"),
		in_intcommon1b(["drawcolor"], "dataread1;>", "\niowrite1;>plot.color\n", "plotter draw line"),
		in_common0(["drawline"], "iowrite1;>plot.line\n", "plotter draw line"),
		in_common0(["drawtri"], "iowrite1;>plot.tri\n", "plotter draw triangle"),
		in_common0(["drawrect"], "iowrite1;>plot.rect\n", "plotter draw rect"),
		in_common0(["drawgetbuff"], "ioread1;>plot.buffer\n", "plotter get buffer content length."),
		in_common0(["drawflush"], "iowrite1;>plot.buffer\n", "plotter flush buffer."),
		in_intcommon1b(["drawfill"], "dataread1;>", "\niowrite1;>plot.fill\n", "plotter fill"),
		in_intcommon1b(["drawfhalt"], "dataread1;>", "\niowrite1;>plot.fhalt\n", "plotter fhalt"),
		in_intcommon1(["set", "set1"], "datawrite1;>", "\n", "set(1) (used after 2-op math, asm code, or get)"),
		in_intcommon1b(["get", "get1"], "dataread1;>", "\n", "get(1) (may be used with set, or asm code)"),
		in_intcommon1(["set2"], "datawrite2;>", "\n", "set2 (used for asm, or get2)"),
		in_intcommon1b(["get2"], "dataread2;>", "\n", "get2 (may be used with set2, and asm code.)"),
		in_common0(["pop", "pop1"], "s2pop1\n", "stack pop (uses stack 2)"),#stack
		in_common0(["peek", "peek1"], "s2peek1\n", "stack peek (uses stack 2)"),
		in_common0(["stackrev"], "s2reverse\n", "stack reverse (uses stack 2)"),
		in_common0(["push", "push1"], "s2push1\n", "stack push (uses stack 2)"),
		in_common0(["pop2"], "s2pop2\n", "stack pop (uses stack 2)"),
		in_common0(["peek2"], "s2peek2\n", "stack peek (uses stack 2)"),
		in_common0(["push2"], "s2push2\n", "stack push (uses stack 2)"),
		in_int2opmath(["add"], "add\n", "add (2op math)"),#alu
		in_int2opmath(["sub"], "sub\n", "subtract (2op math)"),
		in_int2opmath(["div"], "div\n", "divide (2op math)"),
		in_int2opmath(["divmod"], "divmod\n", "divide modulo (2op math)"),
		in_int2opmath(["mul"], "mul\n", "multiply (2op math)"),
		in_labelgoto(), 
		in_int2opcopy(),
		in_int2opswap(),
		in_rrange(),
		in_keyprompt(),
		in_val(),
		in_const(),
		in_marker(),
		in_invert(),
		in_print(),
		in_rawasm(),
		in_getchar(),
		in_vdistat(),
		in_fcon_break(),
		in_fcon_end(),
		in_fcon_loop(),
		in_fcon_begin(),
		in_fcon_ignore(),
		in_fcon_top(),
		in_for(),
		in_condgoto(["if"], "gotoif", condmode=0),#conditionals
		in_condgoto(["ifmore"], "gotoifmore", condmode=0),
		in_condgoto(["ifless"], "gotoifless", condmode=0),
		in_condgoto(["ifnot"], "gotoif", condmode=1),
		in_condgoto(["ifnotmore"], "gotoifmore", condmode=1),
		in_condgoto(["ifnotless"], "gotoifless", condmode=1),
		in_condgoto(["ifrange"], "gotoifmore", condmode=2, gotoop2="gotoifless"),
		in_condgoto(["ifnotrange"], "gotoifmore", condmode=3, gotoop2="gotoifless"),
		in_whileuntil(["while"], "gotoif", condmode=0),#while/until
		in_whileuntil(["whilemore"], "gotoifmore", condmode=0),
		in_whileuntil(["whileless"], "gotoifless", condmode=0),
		in_whileuntil(["until"], "gotoif", condmode=1),
		in_whileuntil(["untilmore"], "gotoifmore", condmode=1),
		in_whileuntil(["untilless"], "gotoifless", condmode=1),
		in_whileuntil(["whilerange"], "gotoifmore", condmode=2, gotoop2="gotoifless"),
		in_whileuntil(["untilrange"], "gotoifmore", condmode=3, gotoop2="gotoifless"),
		in_common0(["return"], "s1pop1\ngotoreg1\n", "return from subroutine."),
		in_common0(["newline"], "fopwri1;:\\n\n", "print newline"),
		in_common0(["space"], "fopwri1;:\\s\n", "print space"),
		in_common0(["stop"], "stop\n", "stop (shutdown vm)"),
		in_common0(["clearcharbuff"], "iowrite1;>io.ttyrd", "Clear TTY input buffer"),
		in_intcommon1b(["dumpd"], "dataread1;>", "\niowrite1;>io.decdump\n", "Dump (decimal)")]
		##############################
		self.bpname=bpname
		self.labels=[]
		self.macros={}
		#run iterative instruction setups:
		for f in ["1", "2", "3", "4"]:
			self.instructs.extend(DO_buffer(f))
			
		self.valid_instructs=[]
		for inst in self.instructs:
			self.valid_instructs.extend(inst.keywords)
	#parse macro definitions
	def p_macrodef(self):
		self.srcobj.seek(0)
		self.srclines_macro=[]
		lineno=0
		for line in self.srcobj:
			line=line.lstrip()
			if line.endswith("\n"):
				line=line[:-1]
			lineno+=1
			if '#' in line:
				line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			for inst in self.instructs:
				if keyword in inst.keywords:
					try:
						
						retvals = inst.pmacro(data, keyword, lineno)
						if retvals!=None:
							if retvals!=[]:
								if retvals[0]==1:
									return 1, retvals[1]
								else:
									for rvar in retvals:
										if rvar.vtype==nptype_macro:
											self.macros[rvar.vname]=rvar
					except AttributeError:
						pass
			self.srclines_macro.append(line)
			#if line.startswith("{"):
			#	print(line)
		return 0, None
		
	def p_preparser(self):
		self.srcobj.seek(0)
		self.srclines=[]
		lineno=0
		for line in self.srclines_macro:
			#line=line.lstrip()
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno+=1
			#macro usage parser
			if line.startswith("!"):
				if not line.endswith(")"):
					return 1, "Parser Error! (line " + str(lineno) + "): split line not terminated with closing ')' !"
				line=line[1:-1]
				
				args=line.split("(", 1)
				#check if name is specified & args are structured correctly
				if len(args)!=2:
					return 1, "Macro Error! (line " + str(lineno) + "): must specify !name(arg,arg2,arg3...)!"
				#check if macro exists
				name, args = args
				args=args.split(",")
				if name not in self.macros:
					return 1, "Macro Error! (line " + str(lineno) + "): Macro '" + name + "' Does not exist."
				#argument count check
				macro_npvar=self.macros[name]
				macro_args=macroarg_count(macro_npvar.vdata)
				if not len(args)==macro_args:
					if not args==[""]:
						return 1, "Macro Error! (line " + str(lineno) + "): Argument Mismatch! '" + str(macro_args) + "' required by '" + name + "'."
				newline=macro_npvar.vdata
				#replace placeholders with code
				argcnt=0
				if "%mod%" in newline:
					try:
						newline=newline.replace("%mod%", macro_npvar.modprefix)
					except AttributeError:
						newline=newline.replace("%mod%", "")
				for f in args:
					#allow for cannonical name(arg, arg, arg) form found in other languages.
					if f.startswith(" "):
						f=f[1:]
					newline=newline.replace("%" + str(argcnt) + "%", f)
					argcnt+=1
				line=newline
			#split_line parser
			if line.startswith("{"):
				if not line.endswith("}"):
					#print(line)
					return 1, "Parser Error! (line " + str(lineno) + "): split line not terminated with closing brace!"
				line=line[1:-1]
				line_subcount=0
				for item in line.split(" / "):
					line_subcount+=1
					self.srclines.append([str(lineno) + "-" + str(line_subcount), item])
			else:
				self.srclines.append([str(lineno) + "-0", line])
		return 0, None
	#parser validation pass
	def p_parsevalid(self):
		#self.srcobj.seek(0)
		#lineno=0
		for line in self.srclines:
			#line=line.lstrip()
			#lineno+=1
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno, line=line
			#if '#' in line:
			#	line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			if keyword not in self.valid_instructs:
				if keyword=="":
					pass
				elif keyword.startswith("#"):
					pass
				else:
					return 1, "Parser Error! (line " + str(lineno) + ") : '" + keyword + "' is not a valid SSTNPL keyword!"
		return 0, None
	#pre-variables syntax check pass
	def p0(self):
		#self.srcobj.seek(0)
		#lineno=0
		for line in self.srclines:
			#line=line.lstrip()
			#lineno+=1
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno, line=line
			#if '#' in line:
			#	line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			for inst in self.instructs:
				if keyword in inst.keywords:
					retval, errordesc = inst.p0(data, keyword, lineno)
					if retval!=0:
						return 1, errordesc
		return 0, None
	
	#constant syntax prepass (used instead of pass 0 for in_include & in_const)
	def p_const(self):
		#self.srcobj.seek(0)
		#lineno=0
		for line in self.srclines:
			#line=line.lstrip()
			#lineno+=1
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno, line=line
			#if '#' in line:
			#	line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			for inst in self.instructs:
				if keyword in inst.keywords:
					try:
						retval, errordesc = inst.p_const(data, keyword, lineno)
						if retval!=0:
							return 1, errordesc
						else:
							if errordesc!=None:
								for f in errordesc:
									if f.vtype==nptype_const:
										set_const(f.vname, f.vdata)
					except AttributeError:
						pass
		return 0, None
	#variable parse & define pass.
	def p1(self):
		#self.srcobj.seek(0)
		#lineno=0
		for line in self.srclines:
			#line=line.lstrip()
			#lineno+=1
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno, line=line
			#if '#' in line:
			#	line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			for inst in self.instructs:
				if keyword in inst.keywords:
					retvars = inst.p1(data, keyword, lineno)
					for rvar in retvars:
						if rvar.vtype==nptype_int:
							self.valid_nvars.extend([rvar.vname])
							self.nvars.extend([rvar])
						if rvar.vtype==nptype_label:
							self.labels.extend([rvar.vname])
						if rvar.vtype==nptype_table:
							self.tables[rvar.vname]=rvar
	#post-variable syntax check pass. (i.e. checking if variable exists.)
	def p2(self):
		#self.srcobj.seek(0)
		#lineno=0
		for line in self.srclines:
			#line=line.lstrip()
			#lineno+=1
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno, line=line
			#if '#' in line:
			#	line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			for inst in self.instructs:
				if keyword in inst.keywords:
					retval, errordesc = inst.p2(data, keyword, lineno, self.nvars, self.valid_nvars, self.labels, self.tables)
					if retval!=0:
						return 1, errordesc
		if not len(fsyntax_stack)==0:
			for block in fsyntax_stack:
				print("    ERROR!: " + block + " Was not terminated.")
			return 1, "Parser: Block termination Error(s). see above!"
			
		return 0, None
	#SBTCVM assembly source code generator pass.
	def p3(self):
		self.outobj.write(headinfo(self.filename, self.bpname))
		#each unique integer variable & literal gets 1 memory address at head of rom.
		for rvar in self.nvars:
			if rvar.vtype==nptype_int and rvar.vname not in self.comped_nvars and rvar.frommodule==0:
				self.outobj.write('null;' + rvar.vdata + ';' + rvar.vname + "\n")
				self.comped_nvars.extend([rvar.vname])
		#self.srcobj.seek(0)
		#lineno=0
		for line in self.srclines:
			#line=line.lstrip()
			#lineno+=1
			#if line.endswith("\n"):
			#	line=line[:-1]
			lineno, line=line
			#if '#' in line:
			#	line=line.rsplit("#", 1)[0]
			try:
				keyword, data = line.split(" ", 1)
			except ValueError:
				keyword = line
				data=""
			for inst in self.instructs:
				if keyword in inst.keywords:
					inst.p3(data, keyword, lineno, self.nvars, self.valid_nvars, self.labels, self.tables, self.outobj)
					
		self.outobj.write("#END OF FILE\n")
		self.outobj.close()
	def mfs(self, mfsfilename):
		mfsfile=open(mfsfilename, "w")
		for f in self.nvars:
			mfsfile.write('int9;' + f.vname + ";" + f.vdata + "\n")
		for f in self.labels:
			mfsfile.write('label;' + f + "\n")
		for f in self.tables:
			rvar=self.tables[f]
			mfsfile.write('table;' + f + ";" + str(rvar.vdata[0]) + ";" + str(rvar.vdata[1]) + "\n")
		for f in localconstants:
			mfsfile.write('const;' + f + ";" + localconstants[f] + "\n")
		for f in self.macros:
			d=self.macros[f]
			mfsfile.write('macro;' + d.vname + ";" + d.vdata + "\n")

		mfsfile.close()
			
	
