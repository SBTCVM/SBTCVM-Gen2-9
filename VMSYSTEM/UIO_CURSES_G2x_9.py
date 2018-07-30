#!/usr/bin/env python
from . import libbaltcalc
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


class uio:
	def __init__(self, cpuref, memref, ioref, statwin, ttywin):
		self.cpu=cpuref
		self.mem=memref
		self.io=ioref
		self.statwin=statwin
		self.ttywin=ttywin
		self.run=1
		ioref.setwritenotify(1, self.ttywrite)
		self.xttycharpos=0
	#status field update loop.
	def statup(self):
		while self.run:
			self.statwin.erase()
			self.statwin.addstr("r1:" + str(self.cpu.reg1.intval) + ", r2:" + str(self.cpu.reg2.intval) + ", in:" + str(self.cpu.instval.intval) + ", da:" + str(self.cpu.dataval.intval) + ", ex:" + str(self.cpu.execpoint.intval))
			self.statwin.refresh()
			time.sleep(0.15)
		return
	#TTY raw line input wrapper.
	def ttyraw(self, string):
		maxy=self.ttywin.getmaxyx()[0]
		self.ttywin.addstr(maxy-1, 0, string)
		self.ttywin.scroll(1)
		self.ttywin.refresh()
		self.xttycharpos=0
	def ttywrite(self, addr, data):
		if data==1:
			self.ttywin.scroll(1)
			self.ttywin.refresh()
			self.xttycharpos=0
		elif int(data) in tcon.dattostr:
			maxy=self.ttywin.getmaxyx()[0]
			self.ttywin.addch(maxy-1, self.xttycharpos, tcon.dattostr[data.intval])
			self.ttywin.refresh()
			self.xttycharpos += 1
			
			