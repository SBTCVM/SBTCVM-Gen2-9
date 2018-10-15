#!/usr/bin/env python

#from . import libbaltcalc
#btint=libbaltcalc.btint
import os
import sys

def adrtosize(adr):
	return adr+9842

def getnonets(romsize):
	return (romsize*2)

def getkilononets(romsize):
	return (romsize*2)/1000.0

def nonetformatted(romsize):
	return str(getnonets(romsize)) + "t9's"

def nonetformatted_smart(romsize):
	size=(romsize*2)
	if size<1000:
		return "" + str(size) + " Nonets [t9]"
	else:
		return "" + str(size/1000.0) + " KiloNonets [Kt9]"


def standardsizeprint(romsize):
	print("\nsize (Nonets): " + nonetformatted_smart(romsize) + " used.")
	print("remaining (Nonets): " + nonetformatted_smart(19683-romsize) + " left.")
	print("\nsize (words) : " + str(romsize) + " words used.")
	print("remaining (words) : " + str(19683-romsize) + " words left.")