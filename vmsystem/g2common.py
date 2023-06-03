#!/usr/bin/env python

# from . import libbaltcalc
# btint=libbaltcalc.btint
import os
import sys

# convert last rom address to rom size.


def adrtosize(adr):
    return adr + 9842

# get romsize in nonets


def getnonets(romsize):
    return (romsize * 2)

# get romsize in KiloNonets


def getkilononets(romsize):
    return (romsize * 2) / 1000.0

# get formatted size in nonets.


def nonetformatted(romsize):
    return str(getnonets(romsize)) + "t9's"

# smart Nonet/KiloNonet romsize formatting function.


def nonetformatted_smart(romsize):
    size = (romsize * 2)
    if size < 1000:
        return "" + str(size) + " Nonets [t9]"
    else:
        return "" + str(size / 1000.0) + " KiloNonets [Kt9]"

# standardized romsize print.


def standardsizeprint(romsize):
    print("\nsize (Nonets): " + nonetformatted_smart(romsize) + " used.")
    print(
        "remaining (Nonets): " +
        nonetformatted_smart(
            19683 -
            romsize) +
        " left.")
    print("\nsize (words) : " + str(romsize) + " words used.")
    print("remaining (words) : " + str(19683 - romsize) + " words left.")

# get size of TROM file.


def gettromsize(romfile):
    romfile.seek(0)
    size = 0
    for word in romfile:
        if "," in word:
            size += 1
    romfile.seek(0)
    return size
