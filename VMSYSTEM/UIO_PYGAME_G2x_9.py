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
pygame.key.set_repeat(200, 50)

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
		self.curxcnt=0
		self.blinkspeed=20
		self.blinkflg=0
		
		self.textfg=(255, 255, 255)
		self.textbg=(0, 0, 0)
		self.TTYbg=(0, 0, 0)
		self.colorkey="+++---"
		self.linebgfill=0
		self.newcol="+++---"
		
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
		#Base TTY IO
		ioref.setwritenotify(1, self.ttywrite)
		ioref.setwritenotify(2, self.tritdump)
		ioref.setwritenotify(3, self.decdump)
		ioref.setreadoverride(4, self.ttyread)
		ioref.setwritenotify(4, self.ttyread)
		ioref.setwritenotify(5, self.packart)
		#Enhanced TTY IO (colors, etc.)
		ioref.setwritenotify(6, self.settextcol)#text fg/bg
		ioref.setwritenotify(7, self.setpackcol)#3 packed art colors as 3, 3-trit RGB values.
		self.xttycharpos=0
		
		####TTY RENDERING
		self.keyinbuff=[]
		self.charcache={}
		self.backfill=monofont.render(" ", True, self.TTYbg, self.TTYbg).convert()
		
		self.gfxpakp=monofont.render(" ", True, (255, 255, 255), (255, 255, 255)).convert()
		self.gfxpak0=monofont.render(" ", True, (127, 127, 127), (127, 127, 127)).convert()
		self.gfxpakn=monofont.render(" ", True, (0, 0, 0), (0, 0, 0)).convert()
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
			if self.gamode==0:
				dcount=0
				fulldraw=0
				uprects=[]
				
				
				
				self.curxcnt+=1
				if self.curxcnt==self.blinkspeed:
					self.curxcnt=0
					if len(self.ttybuff)>0:
						pass
					elif self.blinkflg:
						self.blinkflg=0
						uprects.append(pygame.draw.line(self.screensurf, self.textfg, (self.charx+2, self.chary), (self.charx+2, self.chary+charheight), 2))
					else:
						self.blinkflg=1
						uprects.append(pygame.draw.line(self.screensurf, self.textbg, (self.charx+2, self.chary), (self.charx+2, self.chary+charheight), 2))
				
				while len(self.ttybuff)>0 and dcount!=30:
					dcount+=1
					char=self.ttybuff.pop(0)
					
					#list codes:
					if isinstance(char, list):
						#When list code 20 is detected, change colors using helper method.
						if char[0]==20:
							self.newcolor(char[1])
						if char[0]==21:
							self.newpackcolor(char[1])
							
						
					#newline handler
					elif char=="\n":
						if self.linebgfill==1:
							self.linebgfill=0
							pxrect=pygame.Rect(self.charx, self.chary, charwidth*self.maxx, charheight)
							pygame.draw.rect(self.screensurf, self.TTYbg, pxrect, 0)
							self.curcnt=self.blinkspeed
						pygame.draw.line(self.screensurf, self.textbg, (self.charx+2, self.chary), (self.charx+2, self.chary+charheight), 2)
						self.screensurf.scroll(0, -charheight)
						self.charx=0
						pygame.draw.rect(self.screensurf, self.TTYbg, self.newline_rect, 0)
						fulldraw=1
						
					#backspace handler
					elif char=="\b":
						if self.charx!=0 and self.pchar!="\n" and self.pchar!="\b":
							#clear cursor
							uprects.append(pygame.draw.line(self.screensurf, self.textbg, (self.charx+2, self.chary), (self.charx+2, self.chary+charheight), 2))
							
							self.charx-=charwidth
							uprect=self.screensurf.blit(self.backfill, (self.charx, self.chary))
							if len(self.ttybuff)<4:
								uprects.append(pygame.draw.line(self.screensurf, self.textfg, (self.charx+2, self.chary), (self.charx+2, self.chary+charheight), 2))
								self.blinkflg=0
								self.curxcnt=0
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
					else:
						#normal character handler
						uprect=self.screensurf.blit(self.charrender(char), (self.charx, self.chary))
						if len(self.ttybuff)<4:
							uprects.append(pygame.draw.line(self.screensurf, self.textfg, (self.charx+2+charwidth, self.chary), (self.charx+2+charwidth, self.chary+charheight), 2))
							self.blinkflg=0
							self.curxcnt=0
						self.charx+=charwidth
						uprects.append(uprect)
				if fulldraw:
					pygame.display.flip()
				else:
					pygame.display.update(uprects)
		self.running=0
		return
	def charrender(self, char):
		if char+self.colorkey in self.charcache:
			return self.charcache[char+self.colorkey]
		else:
			chtx=monofont.render(char, True, self.textfg, self.textbg).convert()
			self.charcache[char+self.colorkey]=chtx
			return chtx
	#don't set colors yet, but add a special list code to TTY buffer.
	def settextcol(self, addr, data):
		newcol=data.bttrunk(9)[3:]
		#print(self.newcol)
		self.ttybuff.append([20, newcol])
	#color setter called by text render upon  TTY render buffer list code 20
	def newcolor(self, newcol):
		self.textfg=getRGB27(newcol[:3])
		self.textbg=getRGB27(newcol[3:])
		#print(self.textbg)
		#print(self.textfg)
		#print(self.newcol)
		self.TTYbg=self.textbg
		self.colorkey=newcol
		self.backfill=monofont.render(" ", True, self.TTYbg, self.TTYbg).convert()
		self.linebgfill=1
		
	#PACKART COLOR SET
	#don't set colors yet, but add a special list code to TTY buffer.
	def setpackcol(self, addr, data):
		newcol=data.bttrunk(9)
		#print(self.newcol)
		self.ttybuff.append([21, newcol])
	#color setter called by text render upon  TTY render buffer list code 21
	def newpackcolor(self, newcol):
		
		self.pakpcol=getRGB27(newcol[:3])
		self.pak0col=getRGB27(newcol[3:6])
		self.pakncol=getRGB27(newcol[6:])
		self.gfxpakp=monofont.render(" ", True, self.pakpcol, self.pakpcol).convert()
		self.gfxpak0=monofont.render(" ", True, self.pak0col, self.pak0col).convert()
		self.gfxpakn=monofont.render(" ", True, self.pakncol, self.pakncol).convert()
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


def getRGB27(string):
	redch=string[0]
	greench=string[1]
	bluech=string[2]
	if redch=="-":
		redre=0
	if redch=="0":
		redre=127
	if redch=="+":
		redre=255
	if greench=="-":
		greenre=0
	if greench=="0":
		greenre=127
	if greench=="+":
		greenre=255
	if bluech=="-":
		bluere=0
	if bluech=="0":
		bluere=127
	if bluech=="+":
		bluere=255
	return (redre, greenre, bluere)


