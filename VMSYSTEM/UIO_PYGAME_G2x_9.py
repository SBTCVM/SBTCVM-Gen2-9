#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import pygame
import time

#each frontend (tk, pygame, curses) will have a specific UIO module, as well as its own main executable script.
#PYGAME FRONTEND

#uiolog=open(os.path.join("CAP", "uio_curses.log"), "w")

pygame.display.init()
pygame.font.init()
screensurf=pygame.display.set_mode((800, 600))
pygame.display.set_caption("SBTCVM Gen2-9", "SBTCVM Gen2-9")


class uio:
	def __init__(self, cpuref, memref, ioref, ttylogname="tty_log.log"):
		self.cpu=cpuref
		self.mem=memref
		self.io=ioref
		
		self.run=1
		#self.ttylog=open(os.path.join("CAP", ttylogname), "w")
		#self.ttylogdata=""
		self.ttylog=iofuncts.logit(ttylogname, 1024)
		self.ttylog.write("frontend: Pygame\nBegin UIO tty log:\n")
		ioref.setwritenotify(1, self.ttywrite)
		ioref.setwritenotify(2, self.tritdump)
		ioref.setwritenotify(3, self.decdump)
		ioref.setreadoverride(4, self.ttyread)
		ioref.setwritenotify(4, self.ttyread)
		self.xttycharpos=0
		self.maxy=30
		self.maxx=80
		self.keyinbuff=[]
		self.shutdown=0
		self.clock=pygame.time.Clock()
	#status field update loop.
	
	def statup(self):
		self.running=1
		while self.run:
			sys.stdout.flush()
			self.clock.tick(30)
			#todo: Get Function & special key input parsing working, and add IO line for TTY read.
			for event in pygame.event.get():
				if event.type==pygame.KEYDOWN:
					keyinp=event.unicode
					if keyinp in tcon.strtodat:
						self.keyinbuff.append(tcon.strtodat[keyinp])
					if event.key==pygame.K_RETURN:
						self.keyinbuff.append(1)
				if event.type==pygame.QUIT:
					self.cpu.exception("User Stop", -50, cancatch=0)
		self.running=0
		return
	def ttyraw(self, string):
		if self.xttycharpos==self.maxx:
			self.xttycharpos=0
			print("")
			self.ttylog.write("\n")
		print(string)
		self.ttylog.write(string+"\n")
		self.xttycharpos=0
	
	def tritdump(self, addr, data):
		datstr=data.bttrunk(9)
		for xnumchar in datstr:
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				self.ttylog.write("\n")
			self.ttylog.write(xnumchar)
			self.xttycharpos += 1
		sys.stdout.write(datstr)
		

	
	def decdump(self, addr, data):
		datstr=str(data.intval).rjust(6)
		for xnumchar in datstr:
			#uiolog.write(xnumchar+  "\n")
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				self.ttylog.write("\n")
			self.ttylog.write(xnumchar)
			self.xttycharpos += 1
		sys.stdout.write(datstr)
	#Ready for basic testing.
	def ttyread(self, addr, data):
		if len(self.keyinbuff)>0:
			return btint(self.keyinbuff.pop(0))
		else:
			return btint(0)
	def ttyreadclearbuff(self, addr, data):
		self.keyinbuff=[]
	def ttywrite(self, addr, data):
		if data==1:
			self.xttycharpos=0
			print("")
			self.ttylog.write("\n")
		elif data==2:
			if self.xttycharpos!=0:
				self.xttycharpos-=1
				#Ensure previous character is actually removed in shell output.
				sys.stdout.write("\b \b")
		elif int(data) in tcon.dattostr:
			if self.xttycharpos==self.maxx:
				
				self.xttycharpos=0

				print("")
				self.ttylog.write("\n")
			#self.ttywin.addch(self.maxy-1, self.xttycharpos, tcon.dattostr[data.intval])
			sys.stdout.write(tcon.dattostr[data.intval])
			self.ttylog.write(tcon.dattostr[data.intval])
			#self.ttywin.refresh()
			self.xttycharpos += 1
			
	def powoff(self):
		#write last of TTY log and close.
		self.run=0
		while self.running:
			time.sleep(0.1)
		return
		