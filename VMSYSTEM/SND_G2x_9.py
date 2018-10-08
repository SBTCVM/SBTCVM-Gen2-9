#!/usr/bin/env python
from . import libbaltcalc
from . import iofuncts
btint=libbaltcalc.btint
import os
import sys

#todo: make mixrate user-settable
mixrate=22050

try:
	import pygame
	import fssynthlib
	pygame.mixer.init(frequency=mixrate, size=-16, channels=2)
	fssynthlib.init(mixrate)
	backend=1
	print("Audio Backend: pygame+fssynthlib")
except ImportError:
	backend=None
	print("Audio Backend: None (no sound)")


#Sound init function.
def initsnd(iosys):
	if backend==None:
		return
	sfx(iosys, 50, 0)
	sfx(iosys, 50, 1)

#voice ids:
#pulse=0
#saw=1
#triangle=2
#noise=3


class chipchan_pyg:
	def __init__(self, channel):
		self.voice=0
		self.vol=1.0
		self.panmode=0
		self.noisesam=fssynthlib.makenoise()
		self.playing=0
		self.freq=440
		self.channel=pygame.mixer.Channel(channel)
	def selvoice(data):
		self.voice=int(data)
		if self.voice>3:
			self.voice=3
		elif self.voice<0:
			self.voice=0
	def pan(data):
		if data>=1:
			self.panmode=1
		elif data<=-1:
			self.panmode=-1
		else:
			self.panmode=0

#random number gen
class sfx:
	def __init__(self, iosys, baseaddr, channel):
		self.chipv=chipchan_pyg(channel)
		iosys.setwritenotify(baseaddr, self.setrandstart)
		iosys.setwritenotify(baseaddr+1, self.setrandend)
	def getrandno(self, addr, data):
		
		
	def setrandstart(self, addr, data):
		self.randstart=int(data)
	def setrandend(self, addr, data):
		self.randend=int(data)