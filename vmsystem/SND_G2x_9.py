#!/usr/bin/env python
try:
import sys
import os
from . import libbaltcalc
except ValueError:
    import libbaltcalc
btint = libbaltcalc.btint

# todo: make mixrate user-settable
mixrate = 22050

# buffer
soundbuffer = 512


# Note on adding audio Backends:
# fssynthlib will pack signed 16bit stereo waveform data into an array.


# Sound init function.
def initsnd(iosys, iosys2):
    if backend is None:
        return
    sfx(iosys, 200, 0)
    sfx(iosys, 210, 1)
    sfx(iosys, 220, 2)
    sfx(iosys, 230, 3)
    sfx(iosys2, 200, 4)
    sfx(iosys2, 210, 5)
    sfx(iosys2, 220, 6)
    sfx(iosys2, 230, 7)


class chipchan_pyg:
    def __init__(self, channel):
        self.voice = 0
        self.vol = 1.0
        self.panmode = 0
        self.noisesam = fssynthlib.makenoise()
        self.playing = 0
        self.freq = 440
        self.pulse = 0.5
        self.channel = pygame.mixer.Channel(channel)
        self.samup = 1
        self.sample = None

    def selvoice(self, data):
        self.voice = int(data)
        if self.voice > 5:
            self.voice = 5
        elif self.voice < 0:
            self.voice = 0
        self.samup = 1

    def setvol(self, data):
        data = int(data) / 10.0
        if data > 1.0:
            data = 1.0
        if data < 0.0:
            data = 0.0
        self.vol = data
        self.updatevol()

    def setpulse(self, data):
        # print(data)
        data = int(data) / 10.0
        # print(data)
        if data > 0.99:
            data = 0.99
        if data < 0.01:
            data = 0.01
        self.pulse = data
        # print(self.pulse)
        self.samup = 1

    def pan(self, data):
        if data >= 1:
            self.panmode = 1
        elif data <= -1:
            self.panmode = -1
        else:
            self.panmode = 0
        self.updatevol()

    def setfreq(self, data):
        data = abs(data)
        if data <= 1:
            data = 1
        self.freq = data
        self.samup = 1

    def play(self, data):
        # fix weird upstrem volume reset bug.
        self.channel.stop()
        self.updatevol()
        if self.samup:
            self.gensample()
        self.channel.play(self.sample, loops=-1)

    def stop(self, data):
        self.channel.stop()

    def gensample(self):
        if self.voice == 0:
            self.sample = pygame.mixer.Sound(fssynthlib.makesquare(self.freq))
        elif self.voice == 1:
            self.sample = pygame.mixer.Sound(fssynthlib.maketri(self.freq))
        elif self.voice == 2:
            self.sample = pygame.mixer.Sound(fssynthlib.makesaw(self.freq))
        elif self.voice == 3:
            self.sample = pygame.mixer.Sound(
                fssynthlib.makepulse(
                    self.freq, duty=self.pulse))
        elif self.voice == 4:
            self.sample = pygame.mixer.Sound(
                fssynthlib.maketrisl(
                    self.freq, duty=self.pulse))
        else:
            self.sample = pygame.mixer.Sound(self.noisesam)
        self.samup = 0

    def updatevol(self):
        if self.panmode == 1:
            self.channel.set_volume(self.vol, 0.0)
        elif self.panmode == -1:
            self.channel.set_volume(0.0, self.vol)
        else:
            self.channel.set_volume(self.vol, self.vol)


try:
    import pygame
    try:
        from . import fssynthlib
    except ValueError:
        import fssynthlib
    pygame.mixer.init(frequency=mixrate, size=-16, channels=2)
    fssynthlib.init(mixrate)
    backend = 1
    # set chipchan to point to pygame+fssynthlib scheme
    chipchan = chipchan_pyg
    print("Audio Backend: pygame+fssynthlib")
except ImportError:
    backend = None
    print("Audio Backend: Dummy (no sound)\nNOTICE: PYGAME NOT FOUND. SOUND WILL NOT BE HEARD.")


# soundchannel
class sfx:
    def __init__(self, iosys, baseaddr, channel):
        self.chipv = chipchan_pyg(channel)
        iosys.setwritenotify(baseaddr + 0, self.selvoice)
        iosys.setwritenotify(baseaddr + 1, self.setvol)
        iosys.setwritenotify(baseaddr + 2, self.pan)
        iosys.setwritenotify(baseaddr + 3, self.pulse)
        iosys.setwritenotify(baseaddr + 4, self.setfreq)
        iosys.setwritenotify(baseaddr + 5, self.play)
        iosys.setwritenotify(baseaddr + 6, self.stop)

    def selvoice(self, addr, data):
        self.chipv.selvoice(int(data))

    def setvol(self, addr, data):
        self.chipv.setvol(int(data))

    def pan(self, addr, data):
        self.chipv.pan(int(data))

    def pulse(self, addr, data):
        self.chipv.setpulse(int(data))

    def setfreq(self, addr, data):
        self.chipv.setfreq(int(data))

    def play(self, addr, data):
        self.chipv.play(int(data))

    def stop(self, addr, data):
        self.chipv.stop(int(data))
