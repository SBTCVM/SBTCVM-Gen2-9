#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys
#from subprocess import call
from . import libtextcon as tcon
from . import g2asmlib
#variable type constants
nptype_int=2
nptype_str=3
nptype_label=4
nptype_table=5


#SSTNPL compiler main routine library.

stnpvers='v0.2.0'
versint=(0, 2, 0)

class npvar:
	def __init__(self, vname, vdata, vtype=nptype_int):
		self.vname=vname
		self.vdata=vdata
		#future proofing
		self.vtype=vtype

tritvalid="+0-pn"
varvalid="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"
reservednames=[""]
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
		destobj.write("#label\n" + "null;;" + args+"--label" + "\n")
		return
		


#used in tandem with tstr statements to create character tables.
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
		destobj.write("#table width=" + w + ", height=" + h + "\n" + "null;;" + args+"--table" + "\n")
		return
		

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


class in_rawasm:
	def __init__(self):
		self.keywords=["a", "asm"]
	def p0(self, args, keyword, lineno):
		print("Embedded assembly code at line: '" + str(lineno) + "': " + args)
		return 0, None
	def p1(self, args, keyword, lineno):
		return [npvar(args, None, vtype=nptype_label)]
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		destobj.write("#___RAW ASSEMBLY CODE___\n#_______NOTE: this corresponds to SSTNPL source line #" + str(lineno) + "\n" + args + "#SSTNPL Source Line: '" + str(lineno) + "' \n")
		return

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

class in_invert:
	def __init__(self):
		self.keywords=["invert"]
		self.comment="invert a variable."
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
		destobj.write("#" + self.comment + "\ndataread1;>" + args + "\ninvert1\ndatawrite1;>" + args + "\n")
		return


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
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
		if yv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
		if tname not in tables:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant table name '" + args + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		tname, xv, yv = args.split(",")
		tabvar=tables[tname]
		if keyword.endswith("2"):
			readop="instread1"
		else:
			readop="dataread1"
		destobj.write('''#SSTNPL table read instruction.
setreg1;10x''' + str(tabvar.vdata[0]) + '''
dataread2;>''' + yv + '''
mul
dataread2;>''' + xv + '''
add
setreg2;10x1
add
setreg2;>''' + tname + '''--table
add
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
		return 0, None
	def p1(self, args, keyword, lineno):
		tname, xv, yv, datav = args.split(",")
		retlist=[]
		if isaliteral(xv):
			retlist.extend(literal_do(xv))
		if isaliteral(yv):
			retlist.extend(literal_do(yv))
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		
		tname, xv, yv, datav = args.split(",")
		if xv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
		if datav not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
		if yv not in valid_nvars:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + args + "'"
		if tname not in tables:
			return 1, keyword+": Line: " + str(lineno) + ": Nonexistant table name '" + args + "'"
		return 0, None
	def p3(self, args, keyword, lineno, nvars, valid_nvars, labels, tables, destobj):
		tname, xv, yv, datav = args.split(",")
		tabvar=tables[tname]
		if keyword.endswith("2"):
			writeop="instwrite1"
		else:
			writeop="datawrite1"
		destobj.write('''#SSTNPL table write instruction.
setreg1;10x''' + str(tabvar.vdata[0]) + '''
dataread2;>''' + yv + '''
mul
dataread2;>''' + xv + '''
add
setreg2;10x1
add
setreg2;>''' + tname + '''--table
add
datawrite1;>tabw--adrbuff--''' + str(lineno) + '''
dataread1;>''' + datav + '''
''' + writeop + ''';;tabw--adrbuff--''' + str(lineno) + '''
''')
		return

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
			
			destobj.write("#goto (extra code stores away return address.)\n" + "setreg1;>goto--jumper-" +  str(lineno) + "\ns1push1\ngoto;>" + args +"--label" + "\nnull;;goto--jumper-" +  str(lineno) + "\n")
		else:
			destobj.write("#goto \n" + "goto;>" + args +"--label" + "\n")
		return

class in_condgoto:
	def __init__(self, keywords, gotoop, condmode=0, gotoop2=None):
		self.keywords=keywords
		self.gotoop=gotoop
		self.gotoop2=gotoop2
		self.condmode=condmode
	#conditional logic selector function.
	def getcond(self, lineno, var0, var1, thirdarg=None):
		if self.condmode==0:
			return '''dataread1;>''' + var0 + '''
dataread2;>''' + var1 + '''
''' + self.gotoop + ''';>goto--branch-''' + str(lineno) + '''
goto;>goto--jumper-''' +  str(lineno)
		if self.condmode==1:
			return '''dataread1;>''' + var0 + '''
dataread2;>''' + var1 + '''
''' + self.gotoop + ''';>goto--jumper-''' + str(lineno) + '''
goto;>goto--branch-''' +  str(lineno)
		#range checks
		if self.condmode==2:
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
		if self.condmode==3:
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
			elif arglist[1]!="return" and arglist[1]!="stop":
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
		return retlist
	def p2(self, args, keyword, lineno, nvars, valid_nvars, labels, tables):
		arglist=args.split(" ")
		#check label for goto and gsub
		if len(arglist)==3 and not arglist[1].startswith("="):
			label=arglist[2]
			if not label in labels:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant label'" + label + "'"
		if arglist[1].startswith("="):
			vnname=arglist[1][1:]
			if vnname not in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant destination variable'" + vname + "'"
			valname=arglist[2]
			if valname not in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant source variable'" + vname + "'"
			
				
		#check goto mode
		if (arglist[1] not in ["goto", "gsub", "stop", "return"]) and (not arglist[1].startswith("=")):
			return 1, keyword+": Line: " + str(lineno) + ": Invalid conditional mode! must be 'goto', 'gsub', 'stop', or 'return' or =[var]"
		#variable check
		for x in arglist[0].split(","):
			if not x in valid_nvars:
				return 1, keyword+": Line: " + str(lineno) + ": Nonexistant variable'" + x + "'"
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
setreg1;>goto--jumper-''' +  str(lineno) + ";goto--branch-" +  str(lineno) + "\ns1push1\ngoto;>" + label + "--label\nnull;;goto--jumper-" +  str(lineno) + "\n")
		#set variable
		elif arglist[1].startswith("="):
			destobj.write('''#conditional set
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
dataread1;>''' + arglist[2] + ";goto--branch-" +  str(lineno) + "\ndatawrite1;>" + arglist[1][1:] + "\nnull;;goto--jumper-" +  str(lineno) + "\n")
		#return from subroutine
		elif arglist[1]=="return":
			destobj.write('''#conditional return
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
s1pop1;''' + ";goto--branch-" +  str(lineno) + "\ngotoreg1\nnull;;goto--jumper-" +  str(lineno) + "\n")
		#conditional stop
		elif arglist[1]=="stop":
			destobj.write('''#conditional stop
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
stop;''' + ";goto--branch-" +  str(lineno) + "\n\nnull;;goto--jumper-" +  str(lineno) + "\n")
		#basic goto
		else:
			destobj.write('''#conditional goto
''' + self.getcond(lineno, var0, var1, thirdarg) + '''
setreg1;>goto--jumper-''' +  str(lineno) + ";goto--branch-" +  str(lineno) + "\ngoto;>" + label + "--label\nnull;;goto--jumper-" +  str(lineno) + "\n")
		return

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


#also handles table string tstr syntax
class in_print:
	def __init__(self):
		self.keywords=["print", "prline", "tstr"]
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
		
			
		for char in args:
			if keyword=="tstr":
				destobj.write("null;:" + tcon.chartoasmchar[char] + "\n")
			else:
				destobj.write("fopwri1;:" + tcon.chartoasmchar[char] + "\n")
		if keyword=="prline":
			destobj.write("fopwri1;:\\n\n")
		
		return


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

def isaliteral(arg):
	if arg.startswith("@"):
		return 1
	if arg.startswith(":"):
		return 1
	if arg.startswith("*"):
		return 1
	return 0

def literal_syntax(arg, keyword, lineno):
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
	
def literal_do(arg):
	if arg.startswith("@"):
		return [npvar(arg, "10x" + arg[1:], vtype=nptype_int)]
	if arg.startswith(":"):
		return [npvar(arg, ":" + arg[1:], vtype=nptype_int)]
	if arg.startswith("*"):
		return [npvar(arg, arg[1:], vtype=nptype_int)]
		


def headinfo(filename, basename):
	return '''#SSTNPL COMPILER ''' + stnpvers + '''
#header
head-rname=''' + basename + '''
head-nspin=stdnsp
fopset1;>io.ttywr
#stnp source file: (autogenerated from) "''' + filename + '''
'''

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
	print("SSTNPL COMPILER STARTUP:")
	mainl=mainloop(sourcefile, destpath, sourcepath, bpname)
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


class mainloop:
	def __init__(self, srcobj, destpath, sourcepath, bpname):
		self.filename=sourcepath
		self.srcobj=srcobj
		self.outobj=open(destpath, "w")
		self.destpath=destpath
		self.nvars=[]
		self.valid_nvars=[]
		self.tables={}
		self.comped_nvars=[]
		self.instructs=[in_var(),
		in_label(),
		in_table(),
		in_tabr(),
		in_tabw(),
		in_tdat(),
		in_uiter(),
		in_diter(),
		in_u2iter(),
		in_d2iter(),
		in_intcommon1b(["dumpt"], "dataread1;>", "\niowrite1;>io.tritdump\n", "Dump (trits)"),
		in_intcommon1b(["abs"], "dataread1;>", "\nabs1\n", "Get abs of var"),
		in_intcommon1b(["nabs"], "dataread1;>", "\nnabs1\n", "Get inverted abs of var"),
		in_intcommon1b(["chardump"], "dataread1;>", "\niowrite1;>io.ttywr\n", "Dump (character)"),#set,get
		in_intcommon1(["set", "set1"], "datawrite1;>", "\n", "set(1) (used after 2-op math, asm code, or get)"),
		in_intcommon1(["get", "get1"], "dataread1;>", "\n", "get(1) (may be used with set, or asm code)"),
		in_intcommon1(["set2"], "datawrite2;>", "\n", "set2 (used for asm, or get2)"),
		in_intcommon1(["get2"], "dataread2;>", "\n", "get2 (may be used with set2, and asm code.)"),
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
		in_marker(),
		in_invert(),
		in_print(),
		in_rawasm(),
		in_getchar(),
		in_condgoto(["if"], "gotoif", condmode=0),#conditionals
		in_condgoto(["ifmore"], "gotoifmore", condmode=0),
		in_condgoto(["ifless"], "gotoifless", condmode=0),
		in_condgoto(["ifnot"], "gotoif", condmode=1),
		in_condgoto(["ifnotmore"], "gotoifmore", condmode=1),
		in_condgoto(["ifnotless"], "gotoifless", condmode=1),
		in_condgoto(["ifrange"], "gotoifmore", condmode=2, gotoop2="gotoifless"),
		in_condgoto(["ifnotrange"], "gotoifmore", condmode=3, gotoop2="gotoifless"),
		in_common0(["return"], "s1pop1\ngotoreg1\n", "return from subroutine."),
		in_common0(["newline"], "fopwri1;:\\n\n", "print newline"),
		in_common0(["space"], "fopwri1;:\\s\n", "print space"),
		in_common0(["stop"], "stop\n", "stop (shutdown vm)"),
		in_common0(["clearcharbuff"], "iowrite1;>io.ttyrd", "Clear TTY input buffer"),
		in_intcommon1b(["dumpd"], "dataread1;>", "\niowrite1;>io.decdump\n", "Dump (decimal)")]
		self.bpname=bpname
		self.labels=[]
	def p0(self):
		self.srcobj.seek(0)
		lineno=0
		for line in self.srcobj:
			lineno+=1
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
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
	def p1(self):
		self.srcobj.seek(0)
		lineno=0
		for line in self.srcobj:
			lineno+=1
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
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
	def p2(self):
		self.srcobj.seek(0)
		lineno=0
		for line in self.srcobj:
			lineno+=1
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
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
		return 0, None
	def p3(self):
		self.outobj.write(headinfo(self.filename, self.bpname))
		for rvar in self.nvars:
			if rvar.vtype==nptype_int and rvar.vname not in self.comped_nvars:
				self.outobj.write('null;' + rvar.vdata + ';' + rvar.vname + "\n")
				self.comped_nvars.extend([rvar.vname])
		self.srcobj.seek(0)
		lineno=0
		for line in self.srcobj:
			lineno+=1
			if line.endswith("\n"):
				line=line[:-1]
			if '#' in line:
				line=line.rsplit("#", 1)[0]
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
	
	