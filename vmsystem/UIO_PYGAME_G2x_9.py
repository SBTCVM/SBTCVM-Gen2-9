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

#uiolog=open(os.path.join("cap", "uio_curses.log"), "w")

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
		self.maxx=81
		self.curxcnt=0
		self.blinkspeed=20
		self.blinkflg=0
		
		self.textfg=(255, 255, 255)
		self.textbg=(0, 0, 0)
		self.TTYbg=(0, 0, 0)
		self.colorkey="+++---"
		self.linebgfill=0
		self.newcol="+++---"
		
		self.plotx=800
		self.ploty=600
		
		self.plotobj=PlotterEngine(ioref, 243, 243, self.plotx, self.ploty, 30)
		
		
		#load and set window icon.
		self.picon=pygame.image.load(os.path.join(*["vmsystem", "GFX", "icon32.png"]))
		pygame.display.set_icon(self.picon)
		
		#Init screen for TTY output. basing size on font properties.
		self.screensurf=pygame.display.set_mode((charwidth*self.maxx, charheight*self.maxy))
		self.gamode=0
		self.ttywide=charwidth*self.maxx
		####
		self.fscreen=0
		self.run=1
		#self.ttylog=open(os.path.join("cap", ttylogname), "w")
		#self.ttylogdata=""
		self.ttylog=iofuncts.logit(ttylogname, 1024)
		self.ttylog.write("frontend: Pygame\nBegin UIO tty log:\n")
		#Base TTY IO
		ioref.setwritenotify(1, self.ttywrite)
		ioref.setwritenotify(2, self.tritdump)
		ioref.setwritenotify(3, self.decdump)
		ioref.setreadoverride(4, self.ttyread)
		ioref.setwritenotify(4, self.ttyreadclearbuff)
		ioref.setwritenotify(5, self.packart)
		#Enhanced TTY IO (colors, etc.)
		ioref.setwritenotify(6, self.settextcol)#text fg/bg
		ioref.setwritenotify(7, self.setpackcol)#3 packed art colors as 3, 3-trit RGB values.
		ioref.setwritenotify(8, self.colorpack)#same format as above, but dump 3 raw pixels instead.
		
		ioref.setwritenotify(500, self.setgamode)
		self.xttycharpos=0
		
		####TTY RENDERING
		self.keyinbuff=[]
		self.charcache={}
		self.colorpackdict={}
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
		self.newmode=None
		self.shutdown=0
		self.clock=pygame.time.Clock()
		pygame.display.set_caption(romname + " - SBTCVM Gen2-9", romname + " - SBTCVM Gen2-9")
		self.mousesys=MouseEngine(ioref, 243, 243, self.plotx, self.ploty, charwidth, charheight)
	#input and display thread
	def statup(self):
		self.running=1
		while self.run:
			sys.stdout.flush()
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type==pygame.KEYDOWN:
					mods=pygame.key.get_mods()
					if event.key==pygame.K_RETURN and mods & pygame.KMOD_ALT:
						if self.fscreen:
							self.fscreen=0
							scbak=self.screensurf.copy()
							self.screensurf=pygame.display.set_mode((self.screensurf.get_width(), self.screensurf.get_height()))
							self.screensurf.blit(scbak, (0, 0))
							pygame.display.flip()
						else:
							self.fscreen=1
							scbak=self.screensurf.copy()
							self.screensurf=pygame.display.set_mode((self.screensurf.get_width(), self.screensurf.get_height()), pygame.FULLSCREEN)
							self.screensurf.blit(scbak, (0, 0))
							pygame.display.flip()
					elif event.key==pygame.K_ESCAPE and mods & pygame.KMOD_ALT:
						self.cpu.exception("User Stop", -50, cancatch=0)
					else:
						keyinp=event.unicode
						if keyinp in tcon.strtodat:
							self.keyinbuff.append(tcon.strtodat[keyinp])
						if event.key==pygame.K_RETURN:
							self.keyinbuff.append(1)
				if event.type==pygame.MOUSEBUTTONDOWN:
					if self.gamode==0:
						self.mousesys.mousedown_ga0(event)
					if self.gamode==30:
						self.mousesys.mousedown_ga30(event)
				if event.type==pygame.MOUSEBUTTONUP:
					if self.gamode==0:
						self.mousesys.mouseup_ga0(event)
					if self.gamode==30:
						self.mousesys.mouseup_ga30(event)
				if event.type==pygame.QUIT:
					self.cpu.exception("User Stop", -50, cancatch=0)
			#if in gamode=0 (TTY mode), draw TTY output.
			if self.newmode!=None:
				self.dogamode(self.newmode)
				self.newmode=None
			if self.gamode==0:
				self.render_dumbtty()
			else:
				self.ttybuff=[]
			if self.gamode==30:
				self.plotobj.draw(self.screensurf)
		self.running=0
		return
		
	def setgamode(self, addr, data):
		self.newmode=int(data)
	def dogamode(self, data):
		
		if self.gamode==30:
			self.plotobj.disable()
		
		if self.fscreen:
			if data==0:
				self.gamode=0
				self.screensurf=pygame.display.set_mode((charwidth*self.maxx, charheight*self.maxy), pygame.FULLSCREEN)
				self.screensurf.fill(self.textbg)
				pygame.display.flip()
				self.mousesys.modechange(data)
			if data==30:
				self.gamode=30
				self.screensurf=pygame.display.set_mode((self.plotx, self.ploty), pygame.FULLSCREEN)
				self.plotobj.enable()
				self.screensurf.fill((127, 127, 127))
				pygame.display.flip()
				self.mousesys.modechange(data)
		else:
			if data==0:
				self.gamode=0
				self.screensurf=pygame.display.set_mode((charwidth*self.maxx, charheight*self.maxy))
				self.screensurf.fill(self.textbg)
				pygame.display.flip()
				self.mousesys.modechange(data)
			if data==30:
				self.gamode=30
				self.screensurf=pygame.display.set_mode((self.plotx, self.ploty))
				self.plotobj.enable()
				self.screensurf.fill((127, 127, 127))
				pygame.display.flip()
				self.mousesys.modechange(data)
	
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
	def colorpack(self, addr, data):
		colset=data.bttrunk(9)
		#print(self.newcol)
		self.ttybuff.append([30, getRGB27(colset[:3])])
		self.ttybuff.append([30, getRGB27(colset[3:6])])
		self.ttybuff.append([30, getRGB27(colset[6:])])
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
			sys.stdout.write(xnumchar)
		

	
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
				#self.ttybuff.append("\n")
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
	
	def charrender(self, char):
		if char+self.colorkey in self.charcache:
			return self.charcache[char+self.colorkey]
		else:
			chtx=monofont.render(char, True, self.textfg, self.textbg).convert()
			self.charcache[char+self.colorkey]=chtx
			return chtx
	def char30(self, color):
		if color in self.colorpackdict:
			return self.colorpackdict[color]
		else:
			cpsurf=monofont.render(" ", True, color, color).convert()
			self.colorpackdict[color]=cpsurf
			return cpsurf
	#GAMODE 0 (dumb tty) rendering engine.
	def render_dumbtty(self):
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
			if self.charx>=self.ttywide and char!="\n":
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
			#list codes:
			if isinstance(char, list):
				#When list code 20 is detected, change colors using helper method.
				if char[0]==20:
					self.newcolor(char[1])
				if char[0]==21:
					self.newpackcolor(char[1])
				if char[0]==30:
					uprect=self.screensurf.blit(self.char30(char[1]), (self.charx, self.chary))
					uprects.append(uprect)
					if len(self.ttybuff)<4:
						uprects.append(pygame.draw.line(self.screensurf, self.textfg, (self.charx+2+charwidth, self.chary), (self.charx+2+charwidth, self.chary+charheight), 2))
						self.blinkflg=0
						self.curxcnt=0
					self.charx+=charwidth
				
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

class MouseEngine:
	def __init__(self, ioref, plotx, ploty, plotrealx, plotrealy, TTYcharw, TTYcharh):
		self.ioref=ioref
		self.plotx=plotx
		self.ploty=ploty
		self.plotrealx=plotrealx
		self.plotrealy=plotrealy
		self.TTYcharw=TTYcharw
		self.TTYcharh=TTYcharh
		self.gamode=0
		self.clickbuff=[]
		self.lockx=0
		self.locky=0
		ioref.setreadoverride(300, self.getevent)
		ioref.setwritenotify(300, self.bufferclear)
		ioref.setreadoverride(301, self.getlockx)
		ioref.setreadoverride(302, self.getlocky)
		ioref.setreadoverride(303, self.getrealx)
		ioref.setreadoverride(304, self.getrealy)
		self.clearbuff=0
	def mousedown_ga30(self, event):
		posy=int(((event.pos[1]/float(self.plotrealy))*self.ploty)-121)
		posx=int(((event.pos[0]/float(self.plotrealx))*self.plotx)-121)
		button=event.button
		self.clickbuff.append([button, posx, posy])
		return
	def mouseup_ga30(self, event):
		posy=int(((event.pos[1]/float(self.plotrealy))*self.ploty)-121)
		posx=int(((event.pos[0]/float(self.plotrealx))*self.plotx)-121)
		button=-event.button
		self.clickbuff.append([button, posx, posy])
		return
	def mousedown_ga0(self, event):
		posx, posy=(event.pos[0]//self.TTYcharw, event.pos[1]//self.TTYcharh)
		button=event.button
		self.clickbuff.append([button, posx, posy])
	def mouseup_ga0(self, event):
		posx, posy=(event.pos[0]//self.TTYcharw, event.pos[1]//self.TTYcharh)
		button=-event.button
		self.clickbuff.append([button, posx, posy])
	def modechange(self, gamode):
		self.gamode=gamode
		self.clearbuff=1
		
	
	###IOBUS CALLBACKS###
	
	def getevent(self, addr, data):
		if self.clearbuff:
			self.clearbuff=0
			self.clickbuff=[]
		if len(self.clickbuff)>0:
			button, self.lockx, self.locky = self.clickbuff.pop(0)
		else:
			button=0
		return btint(button)
	def bufferclear(self, addr, data):
		self.clearbuff=1
	def getlockx(self, addr, data):
		return btint(self.lockx)
	def getlocky(self, addr, data):
		return btint(self.locky)
	def getrealx(self, addr, data):
		mpos=pygame.mouse.get_pos()
		if self.gamode==0:
			return btint(mpos[0]//self.TTYcharw)
		if self.gamode==30:
			return btint(int(((mpos[0]/float(self.plotrealx))*self.plotx)-121))
	def getrealy(self, addr, data):
		mpos=pygame.mouse.get_pos()
		if self.gamode==0:
			return btint(mpos[1]//self.TTYcharh)
		if self.gamode==30:
			return btint(int(((mpos[1]/float(self.plotrealy))*self.ploty)-121))

class PlotterEngine:
	def __init__(self, ioref, xsize, ysize, realx, realy, itemlimit=30):
		self.xsize=xsize
		self.ysize=ysize
		self.drawbuff=[]
		self.itemlimit=itemlimit
		self.realx=realx
		self.realy=realy
		self.xmag=realx/float(xsize)
		self.ymag=realy/float(ysize)
		self.active=0
		self.x1=0
		self.y1=0
		self.x2=0
		self.y2=0
		self.color=(127, 127, 127)
		self.widthr=1
		self.heightr=1
		
		ioref.setwritenotify(501, self.dx1)
		ioref.setwritenotify(502, self.dy1)
		ioref.setwritenotify(503, self.dx2)
		ioref.setwritenotify(504, self.dy2)
		ioref.setwritenotify(505, self.dcolor)
		ioref.setwritenotify(506, self.line)
		ioref.setwritenotify(507, self.fill)
		ioref.setwritenotify(508, self.rect)
		ioref.setwritenotify(509, self.widthset)
		ioref.setwritenotify(510, self.heightset)
		ioref.setwritenotify(520, self.fhalt)
		ioref.setwritenotify(521, self.flush)
		ioref.setreadoverride(521, self.buffsize)
	def flush(self, addr, data):
		self.drawbuff=[]
	def buffsize(self, addr, data):
		return btint(len(self.drawbuff))
	def dx1(self, addr, data):
		self.x1=int(data)+121
	def dx2(self, addr, data):
		self.x2=int(data)+121
	def dy1(self, addr, data):
		self.y1=int(data)+121
	def dy2(self, addr, data):
		self.y2=int(data)+121
	
	def widthset(self, addr, data):
		self.widthr=int(data)
		if self.widthr<=0:
			self.widthr=1
	def heightset(self, addr, data):
		self.heightr=int(data)
		if self.heightr<=0:
			self.heightr=1
	def dcolor(self, addr, data):
		newcol=data.bttrunk(9)
		R=getGREY27(newcol[:3])
		G=getGREY27(newcol[3:6])
		B=getGREY27(newcol[6:])
		self.color=(R, G, B)
	def line(self, addr, data):
		self.drawbuff.append([1, self.x1, self.y1, self.x2, self.y2, self.color])
	def rect(self, addr, data):
		self.drawbuff.append([2, self.x1, self.y1, self.widthr, self.heightr, self.color])
	def fill(self, addr, data):
		newcol=data.bttrunk(9)
		R=getGREY27(newcol[:3])
		G=getGREY27(newcol[3:6])
		B=getGREY27(newcol[6:])
		self.drawbuff.append([0, (R, G, B)])
	def fhalt(self, addr, data):
		self.drawbuff.append([-1])
	def draw(self, surface):
		cnt=0
		uprects=[]
		fullup=0
		surface.lock()
		while len(self.drawbuff)>0 and cnt!=self.itemlimit:
			cnt+=1
			
			chunk=self.drawbuff.pop(0)
			if chunk[0]==-1:
				break
			if chunk[0]==0:
				surface.fill(chunk[1])
				fullup=1
			if chunk[0]==1:
				uprects.append(pygame.draw.line(surface, chunk[5], (int(chunk[1]*self.xmag), int(chunk[2]*self.ymag)), (int(chunk[3]*self.xmag), int(chunk[4]*self.ymag))))
			if chunk[0]==2:
				drect=pygame.Rect((int(chunk[1]*self.xmag), int(chunk[2]*self.ymag)), (int(chunk[3]*self.xmag), int(chunk[4]*self.ymag)))
				uprects.append(pygame.draw.rect(surface, chunk[5], drect, 0))

		surface.unlock()
		if fullup:
			pygame.display.flip()
		else:
			pygame.display.update(uprects)
	def enable(self):
		self.active=1
	def disable(self):
		self.active=0

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


def getGREY27(lookupcode):
	if lookupcode=="---":
		return(0)
	if lookupcode=="--0":
		return(10)
	if lookupcode=="--+":
		return(20)
	if lookupcode=="-0-":
		return(31)
	if lookupcode=="-00":
		return(43)
	if lookupcode=="-0+":
		return(54)
	if lookupcode=="-+-":
		return(64)
	if lookupcode=="-+0":
		return(74)
	if lookupcode=="-++":
		return(82)
	if lookupcode=="0--":
		return(92)
	if lookupcode=="0-0":
		return(99)
	if lookupcode=="0-+":
		return(110)
	if lookupcode=="00-":
		return(117)
	if lookupcode=="000":
		return(127)
	if lookupcode=="00+":
		return(138)
	if lookupcode=="0+-":
		return(145)
	if lookupcode=="0+0":
		return(156)
	if lookupcode=="0++":
		return(163)
	if lookupcode=="+--":
		return(173)
	if lookupcode=="+-0":
		return(181)
	if lookupcode=="+-+":
		return(191)
	if lookupcode=="+0-":
		return(201)
	if lookupcode=="+00":
		return(212)
	if lookupcode=="+0+":
		return(222)
	if lookupcode=="++-":
		return(235)
	if lookupcode=="++0":
		return(245)
	if lookupcode=="+++":
		return(255)
