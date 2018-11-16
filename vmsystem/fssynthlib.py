#!/usr/bin/env python
import math
import array
import time
import sys
import random
mixrate=22050
#mixrate=8000
#mixrate=48000

#FSSS Synthesis library
#v1.1.0
verlst=[1, 1, 0]
verstr="v1.1.0"


def init(mixerrate):
	global mixrate
	'''
	Pleas pass mixer rate to library.
	Audio data is generated in signed 16bit ONLY.
	'''
	mixrate=mixerrate

def tangentcap(num):
	if num>18000:
		return 18000
	elif num<-18000:
		return -18000
	else:
		return num
def foobsin_tangent_distort(num):
	return tangentcap(math.floor(math.tan(num)) * 8300) +9000

def foobsin_square(num):
	return (math.floor(math.sin(num)) * 32765) + 15000

def foobsin_sine(num):
	return int(math.sin(num) * 18350)



#generate square wave
def makesquare(freq):
	return array.array('i', [ewchunk(foobsin_square(2.0 * math.pi * freq * t / mixrate)) for t in xrange(0, int(mixrate/freq))])

def makesine(freq):
	return array.array('i', [ewchunk(foobsin_sine(2.0 * math.pi * freq * t / mixrate)) for t in xrange(0, int(mixrate/freq))])

#classic FSSS distorted tangent sound.
def makedistangent(freq):
	freq=freq/2.0
	return array.array('i', [ewchunk(foobsin_tangent_distort(2.0 * math.pi * freq * t / mixrate)) for t in xrange(0, int(mixrate/freq))])



def pulser(num, duty):
	if num<duty:
		return 16370
	else:
		return -16370

#generate pulse wave
#duty should be higher than 0 and less than 1
def makepulse(freq, duty=0.5):
	swtime=int(mixrate/freq)*float(duty)
	return array.array('i', [ewchunk(pulser(t, swtime)) for t in xrange(0, int(mixrate/freq))])


#generate sawtooth wave.
def makesaw(freq):
	sawramp=1.0/(mixrate/float(freq))
	return array.array('i', [ewchunk(((sawramp * t) * 32765) - 15000) for t in xrange(0, int(mixrate/freq))])

def trihelp(num, trifall, rangesize, t):
	if t<trifall:
		return num * t
	else:
		return num * abs(t - rangesize)

def maketri(freq):
	rangesize=int(mixrate/freq)
	quarter=rangesize//4
	triramp=2.0/(mixrate/float(freq))
	trifall=int((mixrate/freq)/2)
	
	return array.array('i', [ewchunk((trihelp(triramp, trifall, rangesize, t) * 36765) - 17000) for t in xrange(0 + quarter, int(mixrate/freq) + quarter)])


##sliding triangle

def trihelp_sl(num, trifall, rangesize, t, numfall):
	if t<trifall:
		return num * t
	else:
		return abs(1.0 - (numfall * abs(t - trifall)))

def maketrisl(freq, duty=0.5):
	dutyflip=((-(duty-0.5))+0.5)
	rangefloat=(mixrate/float(freq))
	rangesize=int(rangefloat)
	quarter=0
	triramp=1.0/((rangefloat*duty))
	trirampfall=1.0/(rangefloat*dutyflip)
	#triramp=(1.0/duty)/(mixrate/float(freq))
	trifall=int(rangefloat*duty)
	
	return array.array('i', [ewchunk((trihelp_sl(triramp, trifall, rangesize, t, trirampfall) * 36765) - 17000) for t in xrange(0 + quarter, int(mixrate/freq) + quarter)])
	
	
#generate white noise sample data.
#only really need to use this one once. since it takes no arguments.
def makenoise():
	return array.array('i', [ewchunk((random.randint(0, 1) * 24765) - 12000) for t in xrange(0, int(mixrate))])

#stereo signed 16bit sound data encoder. intended for use in array generator.
#takes value of foobsin calculation and returns 2 joined, signed 16bit datavalues for wave data.

def ewchunk(data):
	dataint=(int(data))
	if dataint>32765:
		dataint=32765
	if dataint<-32765:
		dataint=-32765
	if dataint<0:
		return -(-dataint<<16 | -dataint)
	else:
		return (dataint<<16 | dataint)
	

#test routines
def test3(freq=110):
	print("Square wave synthesis test (test 1) Freq: '" + str(freq) + "'")
	sound1=pygame.mixer.Sound(makesquare(freq))
	chan=pygame.mixer.Channel(1)
	print('Center')
	chan.set_volume(1, 1)
	chan.play(sound1, -1)
	time.sleep(1)
	print('Left')
	chan.set_volume(1, 0)
	time.sleep(1)
	print('Right')
	chan.set_volume(0, 1)
	time.sleep(1)
	chan.stop()



def test8(freq=110):
	print("Sliding trinagle synthesis test (sweep) (test 1) Freq: '" + str(freq) + "'")
	chan=pygame.mixer.Channel(1)
	chan.set_volume(1, 1)
	for duty in [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]:
		print("duty: '" + str(duty) + "'")
		sound1=pygame.mixer.Sound(maketrisl(freq, duty))
		chan.play(sound1, -1)
		time.sleep(0.25)

def test4(freq=110):
	print("Pulse wave synthesis test (sweep) (test 1) Freq: '" + str(freq) + "'")
	chan=pygame.mixer.Channel(1)
	chan.set_volume(1, 1)
	for duty in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
		print("duty: '" + str(duty) + "'")
		sound1=pygame.mixer.Sound(makepulse(freq, duty))
		chan.play(sound1, -1)
		time.sleep(0.25)

def test1():
	print("White noise synthesis test (test 2)")
	sound1=pygame.mixer.Sound(makenoise())
	chan=pygame.mixer.Channel(1)
	print('Center')
	chan.set_volume(1, 1)
	chan.play(sound1, -1)
	time.sleep(1)
	print('Left')
	chan.set_volume(1, 0)
	time.sleep(1)
	print('Right')
	chan.set_volume(0, 1)
	time.sleep(1)
	chan.stop()

def test2(freq=110):
	print("saw wave synthesis test (test 3) Freq: '" + str(freq) + "'")
	sound1=pygame.mixer.Sound(makesaw(freq))
	chan=pygame.mixer.Channel(1)
	print('Center')
	chan.set_volume(1, 1)
	chan.play(sound1, -1)
	time.sleep(1)
	print('Left')
	chan.set_volume(1, 0)
	time.sleep(1)
	print('Right')
	chan.set_volume(0, 1)
	time.sleep(1)
	chan.stop()

def test5(freq=110):
	print("Sine wave synthesis test (test 5) Freq: '" + str(freq) + "'")
	sound1=pygame.mixer.Sound(makesine(freq))
	chan=pygame.mixer.Channel(1)
	print('Center')
	chan.set_volume(1, 1)
	chan.play(sound1, -1)
	time.sleep(1)
	print('Left')
	chan.set_volume(1, 0)
	time.sleep(1)
	print('Right')
	chan.set_volume(0, 1)
	time.sleep(1)
	chan.stop()

def test6(freq=110):
	print("Distorted tangent wave synthesis test (test 6) Freq: '" + str(freq) + "'")
	sound1=pygame.mixer.Sound(makedistangent(freq))
	chan=pygame.mixer.Channel(1)
	print('Center')
	chan.set_volume(1, 1)
	chan.play(sound1, -1)
	time.sleep(1)
	print('Left')
	chan.set_volume(1, 0)
	time.sleep(1)
	print('Right')
	chan.set_volume(0, 1)
	time.sleep(1)
	chan.stop()


def test7(freq=110):
	print("Triangle wave synthesis test (test 7) Freq: '" + str(freq) + "'")
	sound1=pygame.mixer.Sound(maketri(freq))
	chan=pygame.mixer.Channel(1)
	print('Center')
	chan.set_volume(1, 1)
	chan.play(sound1, -1)
	time.sleep(1)
	print('Left')
	chan.set_volume(1, 0)
	time.sleep(1)
	print('Right')
	chan.set_volume(0, 1)
	time.sleep(1)
	chan.stop()

if __name__=="__main__":
	import pygame
	print("FSSS Synthesis library " + verstr)
	pygame.mixer.init(frequency=mixrate, size=-16, channels=2)
	#print(makesaw(110))
	print("Running Self tests...")
	#noise
	test1()
	#sawtooth
	test2(27)
	test2(55)
	test2(110)
	test2(220)
	test2(440)
	#square wave
	test3(27)
	test3(55)
	test3(110)
	test3(220)
	test3(440)
	#pulse wave (test will sweep a range of pulse widths.)
	test4(27)
	test4(55)
	test4(110)
	test4(220)
	test4(440)
	#Sine wave
	test5(55)
	test5(110)
	test5(220)
	test5(440)
	test5(880)
	#distorted tangent wave
	test6(27)
	test6(55)
	test6(110)
	test6(220)
	test6(440)
	#Triangle wave
	test7(55)
	test7(110)
	test7(220)
	test7(440)
	test7(880)
	#Triangle wave (test will sweep a range of pulse widths.)
	### expect pops. pop reduction too complex.
	test8(55)
	test8(110)
	test8(220)
	test8(440)
	test8(880)