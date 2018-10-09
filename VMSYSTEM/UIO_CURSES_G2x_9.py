#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
import curses
import time

#each frontend (tk, pygame, curses) will have a specific UIO module, as well as its own main executable script.
#due to limitations, curses will be a subset of the main architecture,
#but still has a status area & a TTY and should have both string-dma and keyinterrupt keyboard mode.
#a mono subset of proper text modes may not be out of the question.

#currently, it uses 2 curses windows: a 2 line status area (statwin), with a tty area (ttywin) using the rest of the lines.
#uiolog=open(os.path.join("CAP", "uio_curses.log"), "w")


class uio:
	def __init__(self, cpuref, memref, ioref, statwin, ttywin, mainwin, ttylogname="tty_log.log"):
		self.cpu=cpuref
		self.mem=memref
		self.io=ioref
		self.statwin=statwin
		self.ttywin=ttywin
		self.mainwin=mainwin
		
		self.run=1
		#self.ttylog=open(os.path.join("CAP", ttylogname), "w")
		#self.ttylogdata=""
		self.ttylog=iofuncts.logit(ttylogname, 1024)
		self.ttylog.write("frontend: Curses\nBegin UIO tty log:\n")
		ioref.setwritenotify(1, self.ttywrite)
		ioref.setwritenotify(2, self.tritdump)
		ioref.setwritenotify(3, self.decdump)
		ioref.setreadoverride(4, self.ttyread)
		ioref.setwritenotify(4, self.ttyread)
		self.xttycharpos=0
		self.maxy=self.ttywin.getmaxyx()[0]
		self.maxx=self.ttywin.getmaxyx()[1]
		self.keyinbuff=[]
		self.shutdown=0
	#status field update loop.
	
	def statup(self):
		self.running=1
		while self.run:
			self.maxy=self.ttywin.getmaxyx()[0]
			self.statwin.erase()
			self.statwin.addstr("r1:" + str(self.cpu.reg1.intval) + ", r2:" + str(self.cpu.reg2.intval) + ", in:" + str(self.cpu.instval.intval) + ", da:" + str(self.cpu.dataval.intval) + ", ex:" + str(self.cpu.execpoint.intval))
			self.statwin.refresh()
			self.ttywin.refresh()
			time.sleep(0.05)
			#todo: Get Function & special key input parsing working, and add IO line for TTY read.
			try:
				keyinp=self.mainwin.getkey()
				if keyinp in tcon.strtodat:
					self.keyinbuff.append(tcon.strtodat[keyinp])
				elif keyinp in tcon.curses_specials:
					self.keyinbuff.append(tcon.strtodat[tcon.curses_specials[keyinp]])
			except curses.error:
				continue
		self.running=0
		return
	def ttyraw(self, string):
		if self.xttycharpos==self.maxx:
			self.xttycharpos=0
			self.ttywin.scroll(1)
			self.ttylog.write("\n")
		self.ttywin.addstr(self.maxy-1, 0, string)
		self.ttywin.scroll(1)
		self.ttylog.write(string+"\n")
		self.ttywin.refresh()
		self.xttycharpos=0
	
	def tritdump(self, addr, data):
		for xnumchar in data.bttrunk(9):
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				self.ttywin.scroll(1)
				self.ttylog.write("\n")
			self.ttywin.addch(self.maxy-1, self.xttycharpos, xnumchar)
			self.ttylog.write(xnumchar)
			#self.ttywin.refresh()
			self.xttycharpos += 1
	
	def decdump(self, addr, data):
		#uiolog.write(" " + str(data.intval) + "\n")
		for xnumchar in str(data.intval).rjust(6):
			#uiolog.write(xnumchar+  "\n")
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				self.ttywin.scroll(1)
				self.ttylog.write("\n")
			self.ttywin.addch(self.maxy-1, self.xttycharpos, xnumchar)
			self.ttylog.write(xnumchar)
			#self.ttywin.refresh()
			self.xttycharpos += 1
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
			self.ttywin.scroll(1)
			#self.ttywin.refresh()
			self.xttycharpos=0
			self.ttywin.move(self.maxy-1, self.xttycharpos)
			self.ttylog.write("\n")
		elif data==2:
			if self.xttycharpos!=0:
				self.xttycharpos-=1
				self.ttywin.addch(self.maxy-1, self.xttycharpos, " ")
				self.ttywin.move(self.maxy-1, self.xttycharpos)
			#else:
			#	self.ttywin.scroll(-1)
			#	self.xttycharpos=self.maxx-1
			#	self.ttywin.addch(self.maxy-1, self.xttycharpos, " ")
		elif int(data) in tcon.dattostr:
			if self.xttycharpos==self.maxx:
				
				self.xttycharpos=0
				self.ttywin.scroll(1)
				self.ttywin.move(self.maxy-1, self.xttycharpos)
				self.ttylog.write("\n")
			self.ttywin.addch(self.maxy-1, self.xttycharpos, tcon.dattostr[data.intval])
			self.ttylog.write(tcon.dattostr[data.intval])
			#self.ttywin.refresh()
			self.xttycharpos += 1
			
	def powoff(self):
		#write last of TTY log and close.
		self.ttylog.close()
		self.run=0
		while self.running:
			time.sleep(0.1)
		return
		