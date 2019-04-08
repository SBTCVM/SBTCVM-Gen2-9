#!/usr/bin/env python

import os
if not os.path.isdir("vmsystem"):
	print("changing to script location...")
	os.chdir(os.path.dirname(os.path.abspath(__file__)))


import vmsystem.libbaltcalc as libbaltcalc
from vmsystem.libbaltcalc import btint
import vmsystem.libtextcon as tcon
import time
import sys
import vmsystem.iofuncts as iofuncts
import vmsystem.g2common as g2com

try:
	import pygame
except ImportError:
	sys.exit("ERROR: pygame not found. (REQUIRED)")
	
	
#just point xrange to range in python3.
vers=sys.version_info[0]
if vers==3:
	xrange=range

def packart_maker(imagepath, notrailnew=0):
	print("converting image...")
	image=pygame.image.load(imagepath)
	xsize=image.get_width()
	ysize=image.get_height()
	#print(image.get_height())
	#print(ysize)
	size=2
	outf=open(imagepath.rsplit(".")[0]+".tas0", 'w')
	outf.write('''#SBTCVM Gen2-9 GFXCON: ternary-packed art conversion.
#image file: ''' + imagepath + "\n")
	outf.write("head-nspin=stdnsp\nfopset1;>io.ttywr\nfopset2;>io.packart\n")
	for coly in xrange(0, ysize):
		buffx=""
		for linex in xrange(0, xsize):
			pixcol = image.get_at((linex, coly))
			level = (pixcol[0] + pixcol[1] + pixcol[2])//3
			if level<85:
				buffx+="-"
			elif level<170:
				buffx+="0"
			else:
				buffx+="+"
			if len(buffx)==9:
				outf.write("fopwri2;" + buffx + "\n")
				size+=1
				buffx=""
		if linex>=81:
			print("WARNING: IMAGE BEYOND MAXIMUM TERNARY PACKED ART WIDTH \n ALLOWED BY PYGAME FRONTEND (81)")
		while len(buffx)<9 and buffx!="":
			buffx+="-"
		if buffx!="":
			outf.write("fopwri2;" + buffx + "\n")
			size+=1
		if coly<ysize-1 or notrailnew==0:
			outf.write("fopwri1;:\\n\n")
		size+=1
		#print(coly)
	outf.close()
	print("Done.")
	print(g2com.nonetformatted_smart(size))
	return

def colart_maker(imagepath, notrailnew=0):
	print("converting image...")
	image=pygame.image.load(imagepath)
	xsize=image.get_width()
	ysize=image.get_height()
	#print(image.get_height())
	#print(ysize)
	size=3
	outf=open(imagepath.rsplit(".")[0]+".tas0", 'w')
	outf.write('''#SBTCVM Gen2-9 GFXCON: ternary-packed art conversion.
#image file: ''' + imagepath + "\n")
	outf.write("head-nspin=stdnsp\nfopset1;>io.ttywr\nfopset2;>io.cpack\n")
	for coly in xrange(0, ysize):
		buffx=""
		for linex in xrange(0, xsize):
			pixcol = image.get_at((linex, coly))
			for level in (pixcol[0], pixcol[1], pixcol[2]):
				if level<85:
					buffx+="-"
				elif level<170:
					buffx+="0"
				else:
					buffx+="+"
			if len(buffx)==9:
				outf.write("fopwri2;" + buffx + "\n")
				size+=1
				buffx=""
		if linex>=81:
			print("WARNING: IMAGE BEYOND MAXIMUM TERNARY PACKED ART WIDTH \n ALLOWED BY PYGAME FRONTEND (81)")
		while len(buffx)<9 and buffx!="":
			buffx+="-"
		if buffx!="":
			outf.write("fopwri2;" + buffx + "\n")
			size+=1
		if coly<ysize-1 or notrailnew==0:
			outf.write("fopwri1;:\\n\n")
		size+=1
		#print(coly)
	outf.write('fopset2;>io.packart\n')
	outf.close()
	print("Done.")
	print(g2com.nonetformatted_smart(size))
	return

def colart_maker_RLE(imagepath, notrailnew=0):
	print("converting image...")
	image=pygame.image.load(imagepath)
	xsize=image.get_width()
	ysize=image.get_height()
	if xsize>=79:
		print("Using Full-TTY-width CPRLE Encoding")
	else:
		print("Image is narrower than TTY. using line-broken CPRLE.")
	#print(image.get_height())
	#print(ysize)
	size=1
	pbuff=None
	bufflen=0
	outf=open(imagepath.rsplit(".")[0]+".tas0", 'w')
	outf.write('''#SBTCVM Gen2-9 GFXCON: ternary-packed art conversion. uses Run-length Encoding.
#Needs to be decoded manually.
#image file: ''' + imagepath + "\n"
'''null;>.DATASIZE
''')
	for coly in xrange(0, ysize):
		buffx=""
		for linex in xrange(0, xsize):
			pixcol = image.get_at((linex, coly))
			for level in (pixcol[0], pixcol[1], pixcol[2]):
				if level<85:
					buffx+="-"
				elif level<170:
					buffx+="0"
				else:
					buffx+="+"
			if len(buffx)==9:
				if buffx==pbuff:
					bufflen+=1
					buffx=""
				elif pbuff==None:
					pbuff=buffx
					buffx=""
					size+=1
					bufflen=0
				else:
					outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
					pbuff=buffx
					buffx=""
					size+=1
					bufflen=0
				buffx=""
		if linex>=81:
			print("WARNING: IMAGE BEYOND MAXIMUM TERNARY PACKED ART WIDTH \n ALLOWED BY PYGAME FRONTEND (81)")
		while len(buffx)<9 and buffx!="":
			buffx+="---"
			linex+=1
		if linex<80 or coly==ysize-1:
			
			outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
			if buffx!="":
				outf.write("raw;10x" + str(bufflen) + "," + buffx + "\n")
			pbuff=None
			size+=1
			bufflen=0
		if (coly<ysize-1) and linex<80:
			outf.write("raw;-,0\n")
		elif coly==ysize-1 and notrailnew==0:
			outf.write("raw;-,0\n")
		outf.write("###LINE DIV\n")
		#print(coly)
	outf.write("null;;.DATASIZE\n")
	outf.close()
	print("Done.")
	print(g2com.nonetformatted_smart(size))
	return



def plot_RLE(imagepath, lineinterpol=0):
	print("converting image into PLRLE plotter image format...")
	image=pygame.image.load(imagepath)
	xsize=image.get_width()
	ysize=image.get_height()
	
	#print(image.get_height())
	#print(ysize)
	size=1
	pbuff=None
	bufflen=0
	outf=open(imagepath.rsplit(".")[0]+".tas0", 'w')
	outf.write('''#SBTCVM Gen2-9 GFXCON: run-length encoded tritmap
#Needs to be decoded manually.
#image file: ''' + imagepath + "\n"
'''null;>.DATASIZE
''')
	for coly in xrange(0, ysize):
		buffx=""
		for linex in xrange(0, xsize):
			pixcol = image.get_at((linex, coly))
			if lineinterpol==0:
				buffx=bin8totrit3(pixcol[0])+bin8totrit3(pixcol[1])+bin8totrit3(pixcol[2])
			else:
				if coly % 2:
					buffx=bin8totrit3(pixcol[0]-5)+bin8totrit3(pixcol[1]-5)+bin8totrit3(pixcol[2]-5)
				else:
					buffx=bin8totrit3(pixcol[0])+bin8totrit3(pixcol[1])+bin8totrit3(pixcol[2])
			if buffx==pbuff:
				bufflen+=1
				buffx=""
			elif pbuff==None:
				pbuff=buffx
				buffx=""
				size+=1
				bufflen=0
			else:
				outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
				pbuff=buffx
				buffx=""
				size+=1
				bufflen=0
		if pbuff!=None:
			outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
		pbuff=None
		buffx=""
		size+=1
		bufflen=0
		outf.write("raw;-,0\n")
		outf.write("###LINE DIV\n")
		#print(coly)
	outf.write("null;;.DATASIZE\n")
	outf.close()
	print("Done.")
	print(g2com.nonetformatted_smart(size))
	return

def bin8totrit3(level):
	if level<0:
		level=0
	if level>255:
		level=255
	#print(level)
	xtemp=btint(int(level/9.44444444)-13)
	#print(xtemp.intval)
	xtemp.changeval(xtemp.dectrunk(3))
	return xtemp.bttrunk(3)

if __name__=="__main__":
	try:
		cmd=sys.argv[1]
	except IndexError:
		cmd=None
	try:
		arg=sys.argv[2]
	except IndexError:
		arg=None
	if cmd in ["-h", "--help"]:
		print('''SBTCVM Gen2-9 gfx conversion utility.
-p(n) [image]     : convert an image into 3-color ternary-packed art,
	and place it in a tas0 file. append n for no trailing newline.
-cp(n) [image]    : convert an image into 27-color ternary packed art, 
	and place it in a tas0 file. append n for no trailing newline.
-cprle(n) [image] : convert an image into 27-color cprle compressed
	packed art image data.
-plrle(i) [image] : convert an image into 9-trit (PLRLE format) rle compressed
	tritmap image. append i for line-based striped interpolation.''')
	elif cmd in ["-v", "--version"]:
		print("SBTCVM Gen2-9 gfx conversion utility. v1.0.0\n" + "part of SBTCVM-Gen2-9 v2.1.0.alpha")
	elif cmd in ["-a", "--about"]:
		print('''SBTCVM Gen2-9 gfx conversion utility.
v1.0.0
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

Copyright (c) 2016-2019 Thomas Leathers and Contributors 

see readme.md for more information and licensing of media.

  SBTCVM Gen2-9 is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Gen2-9 is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Gen2-9. If not, see <http://www.gnu.org/licenses/>
  
  ''')
	elif cmd in ["-p"]:
		print("Ternary-Packed art encoder.")
		packart_maker(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1))
		
	elif cmd in ["-cp"]:
		print("Color Ternary-Packed art encoder.")
		colart_maker(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1))
	elif cmd in ["-pn"]:
		print("Ternary-Packed art encoder.")
		packart_maker(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1), 1)
		
	elif cmd in ["-cpn"]:
		print("Color Ternary-Packed art encoder.")
		colart_maker(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1), 1)
	
	elif cmd in ["-cprle"]:
		print("Color Ternary-Packed art encoder (RLE compressed).")
		colart_maker_RLE(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1))
	elif cmd in ["-cprlen"]:
		print("Color Ternary-Packed art encoder (RLE compressed).")
		colart_maker_RLE(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1), 1)
	elif cmd in ["-plrle"]:
		print("RLE-encoded 9-trit RGB tritmap.")
		plot_RLE(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1))
	elif cmd in ["-plrlei"]:
		print("RLE-encoded 9-trit RGB tritmap. (line interpolated)")
		plot_RLE(iofuncts.findtrom(arg, ext=".png", exitonfail=1, exitmsg="image file was not found. STOP", dirauto=1), 1)

	elif cmd == None:
		print("Tip: try gfxcon.py -h for help.")
