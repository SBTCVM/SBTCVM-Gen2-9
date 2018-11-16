#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
from . import libtextcon as tcon
import os
import sys
#try both py3 and py2's Tkinter name.
try:
	import Tkinter as tk
except ImportError:
	import tkinter as tk
except ImportError:
	sys.exit("Error: You must have python Tkinter installed to use SBTCVM's Tkinter Frontend.\nif it is, ensure you run SBTCVM using the python installation that has it.")
import time

#each frontend (tk, pygame, curses) will have a specific UIO module, as well as its own main executable script.
#The TK frontend should be more-or-less fully featured.





class uio:
	def __init__(self, cpuref, memref, ioref, ttylogname="tty_log_tk.log"):
		self.cpu=cpuref
		self.mem=memref
		self.io=ioref
		self.run=1
		#self.ttylog=open(os.path.join("cap", ttylogname), "w")
		#self.ttylogdata=""
		self.ttylog=iofuncts.logit(ttylogname, 1024)
		self.ttylog.write("frontend: TK\nBegin UIO tty log:\n")
		ioref.setwritenotify(1, self.ttywrite)
		ioref.setwritenotify(2, self.tritdump)
		ioref.setwritenotify(3, self.decdump)
		self.maxy=self.ttywin.getmaxyx()[0]
		self.maxx=self.ttywin.getmaxyx()[1]
	#status field update loop.
	
	def statup(self):
		
		while self.run:
			
			time.sleep(0.05)
			
			
		return
	#TTY raw line input wrapper.
	def ttyraw(self, string):
		return
	
	def tritdump(self, addr, data):
		return
	
	def decdump(self, addr, data):
		return
			
	
	def ttywrite(self, addr, data):
		return
			
	def powoff(self):
		#write last of TTY log and close.
		self.ttylog.close()
		self.run=0