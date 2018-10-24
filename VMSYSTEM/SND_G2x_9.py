#!/usr/bin/env python
try:
	from . import libbaltcalc
except ValueError:
	import libbaltcalc
btint=libbaltcalc.btint
import os
import sys

#todo: make mixrate user-settable
mixrate=22050


#Note on adding audio Backends:
#fssynthlib will pack signed 16bit stereo waveform data into an array.



#Sound init function.
def initsnd(iosys):
	if backend==None:
		return
	sfx(iosys, 50, 0)
	sfx(iosys, 50, 1)



class chipchan_pyg:
	def __init__(self, channel):
		self.voice=0
		self.vol=1.0
		self.panmode=0
		self.noisesam=fssynthlib.makenoise()
		self.playing=0
		self.freq=440
		self.pulse=0.5
		self.channel=pygame.mixer.Channel(channel)
		self.samup=1
		self.sample=None
	def selvoice(self, data):
		self.voice=int(data)
		if self.voice>5:
			self.voice=5
		elif self.voice<0:
			self.voice=0
		self.samup=1
	def setvol(self, data):
		data=int(data)/10.0
		if data>1.0:
			data=1.0
		if data<0.0:
			data=0.0
		self.vol=data
		self.updatevol()
	def pulse(self, data):
		data=int(data)/10.0
		if data>1.0:
			data=0.99
		if data<0.0:
			data=0.01
		self.pulse=data
			
	def pan(self, data):
		if data>=1:
			self.panmode=1
		elif data<=-1:
			self.panmode=-1
		else:
			self.panmode=0
		self.updatevol()
	def setfreq(self, data):
		data=abs(data)
		if data<=1:
			data=1
		self.freq=data
		self.samup=1
	def play(self, fadein):
		if self.samup:
			self.gensample()
		fadein=int(fadein)
		if fadein<0:
			fadein=0
		self.channel.play(self.sample, loops = -1, fade_ms=fadein)
	def stop(self, fadeout):
		fadeout=int(fadeout)
		if fadeout<10:
			fadeout=10
		self.channel.fadeout(fadeout)
	def gensample(self):
		if self.voice==0:
			self.sample=pygame.mixer.Sound(fssynthlib.makesquare(self.freq))
		elif self.voice==1:
			self.sample=pygame.mixer.Sound(fssynthlib.maketri(self.freq))
		elif self.voice==2:
			self.sample=pygame.mixer.Sound(fssynthlib.makesaw(self.freq))
		elif self.voice==3:
			self.sample=pygame.mixer.Sound(fssynthlib.makepulse(self.freq, duty=self.pulse))
		elif self.voice==4:
			self.sample=pygame.mixer.Sound(fssynthlib.maketrisl(self.freq, duty=self.pulse))
		else:
			self.sample=pygame.mixer.Sound(self.noisesam)
		self.samup=0
	def updatevol(self):
		if self.panmode==1:
			self.channel.set_volume(self.vol, 0.0)
		elif self.panmode==-1:
			self.channel.set_volume(0.0, self.vol)
		else:
			self.channel.set_volume(self.vol, self.vol)



try:
	import pygame
	import fssynthlib
	pygame.mixer.init(frequency=mixrate, size=-16, channels=2)
	fssynthlib.init(mixrate)
	backend=1
	#set chipchan to point to pygame+fssynthlib scheme
	chipchan=chipchan_pyg
	print("Audio Backend: pygame+fssynthlib")
except ImportError:
	backend=None
	print("Audio Backend: None (no sound)")



#random number gen
class sfx:
	def __init__(self, iosys, baseaddr, channel):
		self.chipv=chipchan_pyg(channel)
		
	def getrandno(self, addr, data):
		return