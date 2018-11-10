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


#TODO: add configuration override for monospace font.
def getmonofont(fontsize):
	global monofont
	fontlist = pygame.font.get_fonts()
	for f in ["mono", "monospace", "monofont"]:
		if f in fontlist:
			monofont = pygame.font.SysFont(f, fontsize)
			return
	for font in fontlist:
		if "mono" in font:
			monofont = pygame.font.SysFont(font, fontsize)
			return
	print("PYGAME FRONTEND: WARNING: Unable to detect monospace font!\nTTY MAY NOT RENDER CORRECTLY.")
	monofont = pygame.font.SysFont(None, fontsize)
	return

#TODO: add configuration override for monospace font size.
#get monospace font, and determine character cell width / height from it.
getmonofont(16)
charwidth=monofont.size("_")[0]
charheight=monofont.size("|_ABC123")[1]


#colors:

textfg=(255, 255, 255)
textbg=(0, 0, 0)
TTYbg=(0, 0, 0)



pygame.display.set_caption("SBTCVM Gen2-9", "SBTCVM Gen2-9")
class uio:
	def __init__(self, cpuref, memref, ioref, romname, ttylogname="tty_log.log"):
		self.cpu=cpuref
		self.mem=memref
		self.io=ioref
		self.pakp="#"
		self.pak0="-"
		self.pakn=" "
		self.maxy=25
		self.maxx=80
		#load and set window icon.
		self.picon=pygame.image.load(os.path.join(*["VMSYSTEM", "GFX", "icon32.png"]))
		pygame.display.set_icon(self.picon)
		
		#Init screen for TTY output. basing size on font properties.
		self.screensurf=pygame.display.set_mode((charwidth*self.maxx, charheight*self.maxy))
		self.gamode=0
		####
		
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
		ioref.setwritenotify(5, self.packart)
		self.xttycharpos=0
		
		####TTY RENDERING
		self.keyinbuff=[]
		self.charcache={}
		self.backfill=monofont.render(" ", True, TTYbg, TTYbg).convert()
		
		self.gfxpakp=monofont.render(" ", True, (210, 210, 255), (210, 210, 255)).convert()
		self.gfxpak0=monofont.render(" ", True, (100, 200, 127), (100, 100, 127)).convert()
		self.gfxpakn=monofont.render(" ", True, (0, 0, 30), (0, 0, 30)).convert()
		self.ttybuff=[]
		self.pchar=""
		self.charx=0
		self.chary=charheight*(self.maxy-1)
		self.newline_rect=pygame.Rect(0, self.chary, charwidth*self.maxx, charheight)
		####
		
		self.shutdown=0
		self.clock=pygame.time.Clock()
		pygame.display.set_caption(romname + " - SBTCVM Gen2-9", romname + " - SBTCVM Gen2-9")
	#status field update loop.
	
	def statup(self):
		self.running=1
		while self.run:
			sys.stdout.flush()
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type==pygame.KEYDOWN:
					keyinp=event.unicode
					if keyinp in tcon.strtodat:
						self.keyinbuff.append(tcon.strtodat[keyinp])
					if event.key==pygame.K_RETURN:
						self.keyinbuff.append(1)
				if event.type==pygame.QUIT:
					self.cpu.exception("User Stop", -50, cancatch=0)
			#if in gamode=0 (TTY mode), draw TTY output.
			if self.gamode==0 and len(self.ttybuff)>0:
				dcount=0
				fulldraw=0
				uprects=[]
				while len(self.ttybuff)>0 and dcount!=30:
					dcount+=1
					char=self.ttybuff.pop(0)
					#newline handler
					if char=="\n":
						self.screensurf.scroll(0, -charheight)
						self.charx=0
						pygame.draw.rect(self.screensurf, TTYbg, self.newline_rect, 0)
						fulldraw=1
					#backspace handler
					elif char=="\b":
						if self.charx!=0 and self.pchar!="\n" and self.pchar!="\b":
							self.charx-=charwidth
							uprect=self.screensurf.blit(self.backfill, (self.charx, self.chary))
							uprects.append(uprect)
					#ternary packed art rendering
					elif char==-1:
						uprect=self.screensurf.blit(self.gfxpakn, (self.charx, self.chary))
						self.charx+=charwidth
						uprects.append(uprect)
					elif char==0:
						uprect=self.screensurf.blit(self.gfxpak0, (self.charx, self.chary))
						self.charx+=charwidth
						uprects.append(uprect)
					elif char==1:
						uprect=self.screensurf.blit(self.gfxpakp, (self.charx, self.chary))
						self.charx+=charwidth
						uprects.append(uprect)
					#normal character handler
					elif char!=" ":
						uprect=self.screensurf.blit(self.charrender(char), (self.charx, self.chary))
						self.charx+=charwidth
						uprects.append(uprect)
					else:
						self.charx+=charwidth
				if fulldraw:
					pygame.display.flip()
				else:
					pygame.display.update(uprects)
		self.running=0
		return
	def charrender(self, char):
		if char in self.charcache:
			return self.charcache[char]
		else:
			chtx=monofont.render(char, True, textfg, textbg).convert()
			self.charcache[char]=chtx
			return chtx
	def ttyraw(self, string):
		if self.xttycharpos==self.maxx:
			self.xttycharpos=0
			print("")
			self.ttybuff.append("\n")
			self.ttylog.write("\n")
		print(string)
		for f in string+"\n":
			self.ttybuff.append(f)
		self.ttylog.write(string+"\n")
		self.xttycharpos=0
	
	def packart(self, addr, data):
		datstr=data.bttrunk(9)
		for xnumchar in datstr:
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				self.ttybuff.append("\n")
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
			self.ttybuff.append(buffval)
			sys.stdout.write(pval)
	def tritdump(self, addr, data):
		datstr=data.bttrunk(9)
		for xnumchar in datstr:
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				self.ttybuff.append("\n")
				self.ttylog.write("\n")
			self.ttylog.write(xnumchar)
			self.xttycharpos += 1
			self.ttybuff.append(xnumchar)
			sys.stdout.write(datstr)
		

	
	def decdump(self, addr, data):
		datstr=str(data.intval).rjust(6)
		for xnumchar in datstr:
			#uiolog.write(xnumchar+  "\n")
			if self.xttycharpos==self.maxx:
				self.xttycharpos=0
				print("")
				self.ttybuff.append("\n")
				self.ttylog.write("\n")
			self.ttylog.write(xnumchar)
			self.xttycharpos += 1
			self.ttybuff.append(xnumchar)
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
			self.ttybuff.append("\n")
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
				self.ttybuff.append("\n")
				print("")
				self.ttylog.write("\n")
			#self.ttywin.addch(self.maxy-1, self.xttycharpos, tcon.dattostr[data.intval])
			tchar=tcon.dattostr[data.intval]
			sys.stdout.write(tchar)
			self.ttylog.write(tchar)
			self.ttybuff.append(tchar)
			#self.ttywin.refresh()
			self.xttycharpos += 1
			
	def powoff(self):
		#write last of TTY log and close.
		self.run=0
		while self.running:
			time.sleep(0.1)
		return
		