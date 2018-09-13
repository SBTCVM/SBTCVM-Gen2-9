#!/usr/bin/env python
from . import libbaltcalc
#import libbaltcalc
btint=libbaltcalc.btint
import os
import sys
#SBTCVM-BTT2: SBTCVM Gen2's next generation text encoding.
#NOTE: while the encoding currently contains ~100 chars, and the latin set
#   begins at MNI(5), various virtual hardware & software of SBTCVM is designed
#   to accept a full 9 trits.

class schr:
	def __init__(self, uchar, asmchar, dataval, chrname=None, dumpstr=None, bldumpstr=None):
		if chrname==None:
			self.chrname=uchar
		else:
			self.chrname=chrname
		if dumpstr==None:
			self.dumpstr=" "+uchar
		else:
			self.dumpstr=dumpstr
		if bldumpstr==None:
			self.bldumpstr=uchar
		else:
			self.bldumpstr=bldumpstr
		
		self.uchar=uchar
		self.asmchar=asmchar
		self.dataval=dataval

def nchr(uchar, dataval):
	#check for normal chars used in assembler syntax. (aka that need escaping) (only vertical bar and semicolon for now)
	if uchar in asmchar_special:
		return schr(uchar, asmchar_special[uchar], dataval, chrname=None, dumpstr=None, bldumpstr=None)
	else:
		return schr(uchar, uchar, dataval, chrname=None, dumpstr=None, bldumpstr=None)

#----------dataset startup code below---------


# master latin bank #1 character reference for SBTCVM-BTT2
#WARNING: THE ORDER OF CHARS IN STRING DETERMINE HOW THEY ARE MAPPED!
#ensure each of these are precisely 27 chars long.
chardata0="""abcdefghijklmnopqrstuvwxyz """
chardata1="""ABCDEFGHIJKLMNOPQRSTUVWXYZ."""
chardata2="""0123456789`-=~!@#$%^&*()_+!"""
chardata3='[]' + "\\" + "{}|;':" + '"' + ',./<>?'


#normal characters that require escaping.
asmchar_special={"|": "\\v", ";": "\\c", "\\": "\\b", " ": "\\s"}

# Special bank #1 (0-??)
#Special case chars (currently newline, backspace, and NULL. all three have fixed positions in datastructure.)

spchars=[schr("\n", "\\n", 1, "newline", "\\n", "."), schr(None, "\\0", 0, "null", "\\0", "."), schr('\b', "\\x", 2, "backspace", "\\x", ".")]
spcharlist_asm=["\\n", "\\0", "\\x"]


curses_specials={'KEY_BACKSPACE': '\b'}

# --- INIT NORMAL CHARACTERS ---
normchars=[]
normcharlist=list(chardata0 + chardata1 + chardata2 + chardata3)

#latin bank #1 (MNI(5)-0)

#assign codes to each of the normal chars algorithmically.
charval=libbaltcalc.mni(5)
#charval=1
for ch in normcharlist:
	normchars.extend([nchr(ch, charval)])
	charval+=1
	#skip special chars (null and newline)
	if charval==0:
		charval+=2



####debug messages (comment out if not working on lib)
#print("SBTCVM-BTT2 (libtextcon): Last assigned normal char: '" + ch + "'")
#print("SBTCVM-BTT2 (libtextcon): next available normal charcode: '" + str(charval) + "'")
#print("SBTCVM-BTT2 (libtextcon): normal chars assigned: " + str(len(normcharlist)))

#build main character list
allchars=normchars+spchars

normal_char_list=normcharlist


#build dict for UIO to use.
dattostr={}
for ch in allchars:
	if ch.uchar!=None:
		dattostr[ch.dataval]=ch.uchar
		
strtodat={}
for ch in allchars:
	if ch.uchar!=None:
		strtodat[ch.uchar]=ch.dataval

#build asm char lookup for compilers
chartoasmchar={}
for ch in allchars:
	if ch.uchar!=None:
		chartoasmchar[ch.uchar]=ch.asmchar

#--- ASSEMBLER DATA STRUCTURES ---

#build raw list of all characters for assembler
allcharlist_asm=normcharlist+spcharlist_asm

#build assembler character data lookup and escaped character reference list.
asm_chrtodat={}
asm_escaped=[]
for ch in allchars:
	if ch.asmchar!=None:
		asm_chrtodat[ch.asmchar]=ch.dataval
	#dynamically add escaped chars to 
	if ch.asmchar.startswith("\\"):
		asm_escaped.extend([ch.asmchar])
		