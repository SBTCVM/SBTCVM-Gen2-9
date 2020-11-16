#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import time
if sys.platform=="win32":
	print("Bare Frontend: using windows mode. WARNING: Input not yet supported.\n please use curses or pygame frontends!")
	#import msvcrt
	#getch=msvcrt.getch
#else:
	
	print("Bare Frontend: using Nix* mode. WARNING: Input not yet supported.\n please use curses or pygame frontends!")
	#import tty
	#import termios
	#def getch():
		#filedesc = sys.stdin.fileno()
		#terminal_old = termios.tcgetattr(filedesc)
		#term_new = termios.tcgetattr(filedesc)
		#term_new[3] 
		#try:
			#sys.stdout.flush()
			#termios.tcflow(sys.stdout.fileno(), termios.TCIOFF)
			
			#tty.setraw(sys.stdin.fileno())
			#char = sys.stdin.read(1)
			#termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, terminal_old)
			#termios.tcflow(sys.stdout.fileno(), termios.TCION)
		#finally:
			
			#termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, terminal_old)
		#return char





class uio:
	def __init__(self, cpuref, memref, ioref, ttylogname="tty_log_bare.log"):
		self.cpu=cpuref
		self.mem=memref
		self.io=ioref
		self.run=1
		self.running=1
		#self.ttylog=open(os.path.join("cap", ttylogname), "w")
		#self.ttylogdata=""
		self.ttylog=iofuncts.logit(ttylogname, 1024)
		self.ttylog.write("frontend: Bare\nBegin UIO tty log:\n")
		ioref.setwritenotify(1, self.ttywrite)
		ioref.setwritenotify(2, self.tritdump)
		ioref.setwritenotify(3, self.decdump)
		ioref.setreadoverride(4, self.ttyread)
		ioref.setwritenotify(4, self.ttyreadclearbuff)
		ioref.setwritenotify(5, self.packart)
		self.ttybuff=[]
		self.keyinbuff=[]
		self.xttycharpos=0
		self.pakp="#"
		self.pak0="-"
		self.pakn=" "
		self.maxx=81
		self.maxy=25
	#status field update loop.
	
	def statup(self):
		
		while self.run:
			time.sleep(0.1)
			#char=""
			#if sys.platform=="win32":
				#while char!=None and self.run:
					#char=getch()
					#if char == '\x08' or char == '\x7f' or char == "\b":
						#self.keyinbuff.append(2)
					#elif char=="\n":
						#self.keyinbuff.append(1)
					#elif char in tcon.strtodat:
						#self.keyinbuff.append(tcon.strtodat[char])
			#else:
				#char=getch()
				#if char!=None:
					#if char == '\x08' or char == '\x7f' or char == "\b":
						#self.keyinbuff.append(2)
					#elif char=="\n":
						#self.keyinbuff.append(1)
					#elif char in tcon.strtodat:
						#self.keyinbuff.append(tcon.strtodat[char])
		self.running=0
		return
	#TTY raw line input wrapper.
	def ttyraw(self, string):
		if self.xttycharpos==self.maxx:
			self.xttycharpos=0
			print("")
			self.ttylog.write("\n")
		print(string)
		self.ttylog.write(string+"\n")
		self.xttycharpos=0
		return
	
	def tritdump(self, addr, data):
		datstr=data.bttrunk(9)
		for xnumchar in datstr:
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				#self.ttybuff.append("\n")
				self.ttylog.write("\n")
			self.ttylog.write(xnumchar)
			self.xttycharpos += 1
			#self.ttybuff.append(xnumchar)
			sys.stdout.write(xnumchar)
	
	def decdump(self, addr, data):
		datstr=str(data.intval).rjust(6)
		for xnumchar in datstr:
			#uiolog.write(xnumchar+  "\n")
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				#self.ttybuff.append("\n")
				self.ttylog.write("\n")
			self.ttylog.write(xnumchar)
			self.xttycharpos += 1
			#self.ttybuff.append(xnumchar)
		sys.stdout.write(datstr)
			
	def packart(self, addr, data):
		datstr=data.bttrunk(9)
		for xnumchar in datstr:
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				#self.ttybuff.append("\n")
				self.ttylog.write("\n")
			if xnumchar=="+":
				pval=self.pakp
				buffval=1
			elif xnumchar=="0":
				pval=self.pak0
				buffval=0
			else:
				pval=self.pakn
				buffval=-1
			self.ttylog.write(pval)
			self.xttycharpos += 1
			#self.ttybuff.append(buffval)
			sys.stdout.write(pval)
		
	def ttyreadclearbuff(self, addr, data):
		self.keyinbuff=[]
		return
			
	def ttyread(self, addr, data):
		if len(self.keyinbuff)>0:
			return btint(self.keyinbuff.pop(0))
		else:
			return btint(0)
			
	def ttywrite(self, addr, data):
		if data==1:
			self.xttycharpos=0
			print("")
			#self.ttybuff.append("\n")
			self.ttylog.write("\n")
		elif data==2:
			if self.xttycharpos!=0:
				self.xttycharpos-=1
				#Ensure previous character is actually removed in shell output.
				sys.stdout.write("\b \b")
				self.ttybuff.append("\b")
		elif int(data) in tcon.dattostr:
			if self.xttycharpos==self.maxx:
				
				self.xttycharpos=0
				#self.ttybuff.append("\n")
				print("")
				self.ttylog.write("\n")
			#self.ttywin.addch(self.maxy-1, self.xttycharpos, tcon.dattostr[data.intval])
			tchar=tcon.dattostr[data.intval]
			sys.stdout.write(tchar)
			self.ttylog.write(tchar)
			#self.ttybuff.append(tchar)
			#self.ttywin.refresh()
			self.xttycharpos += 1
		return
			
	def powoff(self):
		#write last of TTY log and close.
		
		self.run=0
		#while self.running:
		#	time.sleep(0.1)
		
		self.ttylog.close()
		return
	