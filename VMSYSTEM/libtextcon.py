#!/usr/bin/env python
from . import libbaltcalc
#import libbaltcalc
btint=libbaltcalc.btint
import os
import sys
#character data

#refrence for SBTCVM-BTT-6-v2 (SBTCVM-BTT2)
#WARNING: THE ORDER OF CHARS IN STRING DETERMINE HOW THEY ARE MAPPED!
chardata0="""abcdefghijklmnopqrstuvwxyz """
chardata1="""ABCDEFGHIJKLMNOPQRSTUVWXYZ."""
chardata2="""0123456789`-=~!@#$%^&*()_+!"""
chardata3='[]' + "\\" + "{}|;':" + '"' + ',./<>?'


#print(len(chardata3))

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
	return schr(uchar, uchar, dataval, chrname=None, dumpstr=None, bldumpstr=None)
#Special case chars (currently newline and NULL
spchars=[schr("\n", "\\n", 1, "newline", "\\n", "."), schr(None, "\\0", 0, "null", "\\0", ".")]

normchars=[]
normcharlist=list(chardata0 + chardata1 + chardata2 + chardata3)
spcharlist_asm=["\\n", "\\0"]
charval=libbaltcalc.mni(6)
for ch in normcharlist:
	normchars.extend([nchr(ch, charval)])
	charval+=1

allchars=normchars+spchars
allcharlist_asm=normcharlist+spcharlist_asm

#build dict for UIO to use.
dattostr={}
for ch in allchars:
	if ch.uchar!=None:
		dattostr[ch.dataval]=ch.uchar

asm_chrtodat={}

for ch in allchars:
	if ch.asmchar!=None:
		asm_chrtodat[ch.asmchar]=ch.dataval