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


# just point xrange to range in python3.
vers = sys.version_info[0]
if vers == 3:
    xrange = range


def packart_maker(imagepath, notrailnew=0):
    print("converting image...")
    image = pygame.image.load(imagepath)
    xsize = image.get_width()
    ysize = image.get_height()
    # print(image.get_height())
    # print(ysize)
    size = 2
    outf = open(imagepath.rsplit(".")[0] + ".tas0", 'w')
    outf.write('''#SBTCVM Gen2-9 GFXCON: ternary-packed art conversion.
#image file: ''' + imagepath + "\n")
    outf.write("head-nspin=stdnsp\nfopset1;>io.ttywr\nfopset2;>io.packart\n")
    for coly in xrange(0, ysize):
        buffx = ""
        for linex in xrange(0, xsize):
            pixcol = image.get_at((linex, coly))
            level = (pixcol[0] + pixcol[1] + pixcol[2]) // 3
            if level < 85:
                buffx += "-"
            elif level < 170:
                buffx += "0"
            else:
                buffx += "+"
            if len(buffx) == 9:
                outf.write("fopwri2;" + buffx + "\n")
                size += 1
                buffx = ""
        if linex >= 81:
            print(
                "WARNING: IMAGE BEYOND MAXIMUM TERNARY PACKED ART WIDTH \n ALLOWED BY PYGAME FRONTEND (81)")
        while len(buffx) < 9 and buffx != "":
            buffx += "-"
        if buffx != "":
            outf.write("fopwri2;" + buffx + "\n")
            size += 1
        if coly < ysize - 1 or notrailnew == 0:
            outf.write("fopwri1;:\\n\n")
        size += 1
        # print(coly)
    outf.close()
    print("Done.")
    print(g2com.nonetformatted_smart(size))
    return


def colart_maker(imagepath, notrailnew=0):
    print("converting image...")
    image = pygame.image.load(imagepath)
    xsize = image.get_width()
    ysize = image.get_height()
    # print(image.get_height())
    # print(ysize)
    size = 3
    outf = open(imagepath.rsplit(".")[0] + ".tas0", 'w')
    outf.write('''#SBTCVM Gen2-9 GFXCON: ternary-packed art conversion.
#image file: ''' + imagepath + "\n")
    outf.write("head-nspin=stdnsp\nfopset1;>io.ttywr\nfopset2;>io.cpack\n")
    for coly in xrange(0, ysize):
        buffx = ""
        for linex in xrange(0, xsize):
            pixcol = image.get_at((linex, coly))
            for level in (pixcol[0], pixcol[1], pixcol[2]):
                if level < 85:
                    buffx += "-"
                elif level < 170:
                    buffx += "0"
                else:
                    buffx += "+"
            if len(buffx) == 9:
                outf.write("fopwri2;" + buffx + "\n")
                size += 1
                buffx = ""
        if linex >= 81:
            print(
                "WARNING: IMAGE BEYOND MAXIMUM TERNARY PACKED ART WIDTH \n ALLOWED BY PYGAME FRONTEND (81)")
        while len(buffx) < 9 and buffx != "":
            buffx += "-"
        if buffx != "":
            outf.write("fopwri2;" + buffx + "\n")
            size += 1
        if coly < ysize - 1 or notrailnew == 0:
            outf.write("fopwri1;:\\n\n")
        size += 1
        # print(coly)
    outf.write('fopset2;>io.packart\n')
    outf.close()
    print("Done.")
    print(g2com.nonetformatted_smart(size))
    return


def colart_maker_RLE(imagepath, notrailnew=0):
    print("converting image...")
    image = pygame.image.load(imagepath)
    xsize = image.get_width()
    ysize = image.get_height()
    if xsize >= 79:
        print("Using Full-TTY-width CPRLE Encoding")
    else:
        print("Image is narrower than TTY. using line-broken CPRLE.")
    # print(image.get_height())
    # print(ysize)
    size = 1
    pbuff = None
    bufflen = 0
    outf = open(imagepath.rsplit(".")[0] + ".tas0", 'w')
    outf.write(
        '''#SBTCVM Gen2-9 GFXCON: ternary-packed art conversion. uses Run-length Encoding.
#Needs to be decoded manually.
#image file: ''' +
        imagepath +
        "\n"
        '''null;>.DATASIZE
''')
    for coly in xrange(0, ysize):
        buffx = ""
        for linex in xrange(0, xsize):
            pixcol = image.get_at((linex, coly))
            for level in (pixcol[0], pixcol[1], pixcol[2]):
                if level < 85:
                    buffx += "-"
                elif level < 170:
                    buffx += "0"
                else:
                    buffx += "+"
            if len(buffx) == 9:
                if buffx == pbuff:
                    bufflen += 1
                    buffx = ""
                elif pbuff is None:
                    pbuff = buffx
                    buffx = ""
                    size += 1
                    bufflen = 0
                else:
                    outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
                    pbuff = buffx
                    buffx = ""
                    size += 1
                    bufflen = 0
                buffx = ""
        if linex >= 81:
            print(
                "WARNING: IMAGE BEYOND MAXIMUM TERNARY PACKED ART WIDTH \n ALLOWED BY PYGAME FRONTEND (81)")
        while len(buffx) < 9 and buffx != "":
            buffx += "---"
            linex += 1
        if linex < 80 or coly == ysize - 1:

            outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
            if buffx != "":
                outf.write("raw;10x" + str(bufflen) + "," + buffx + "\n")
            pbuff = None
            size += 1
            bufflen = 0
        if (coly < ysize - 1) and linex < 80:
            outf.write("raw;-,0\n")
        elif coly == ysize - 1 and notrailnew == 0:
            outf.write("raw;-,0\n")
        outf.write("###LINE DIV\n")
        # print(coly)
    outf.write("null;;.DATASIZE\n")
    outf.close()
    print("Done.")
    print(g2com.nonetformatted_smart(size))
    return


def plot_BIN_RLE(imagepath, lineinterpol=0):
    print("converting image into BINRLE plotter image format...")
    image = pygame.image.load(imagepath)
    xsize = image.get_width()
    ysize = image.get_height()
    pixcol = None
    # print(image.get_height())
    # print(ysize)
    size = 1
    pbuff = None
    bufflen = 0
    bank = 1
    # find initial color state
    if lineinterpol == 0:
        color_bool = binencode(image.get_at((0, 0)), offset=0)
    elif lineinterpol == 2:
        color_bool = binencode(image.get_at((0, 0)), offset=-51 - 25)
    else:
        color_bool = binencode(image.get_at((0, 0)), offset=42)
    outf = open(imagepath.rsplit(".")[0] + ".tas0", 'w')
    outf.write('''#SBTCVM Gen2-9 GFXCON: run-length encoded tritmap
#Needs to be decoded manually.
#image file: ''' + imagepath + "\n"
               '''raw;10x''' + str(xsize) + ''',10x''' + str(color_bool) + '''
''')
    for coly in xrange(0, ysize):
        for linex in xrange(0, xsize):
            pixcol = image.get_at((linex, coly))
            if lineinterpol == 0:
                buffx = binencode(pixcol, offset=0)
            elif lineinterpol == 2:
                if coly % 4 == 0:
                    buffx = binencode(pixcol, offset=-51 - 25)
                elif coly % 4 == 1:
                    buffx = binencode(pixcol, offset=-51 + 25)
                elif coly % 4 == 2:
                    buffx = binencode(pixcol, offset=51 - 25)
                else:
                    buffx = binencode(pixcol, offset=51 + 25)
            else:
                if coly % 2:
                    buffx = binencode(pixcol, offset=-42)
                else:
                    buffx = binencode(pixcol, offset=42)
            if buffx == pbuff:
                bufflen += 1
            elif pbuff is None:
                pbuff = buffx

                bufflen = 0
            else:
                bufflen, bank, size = binformat(bufflen, bank, outf, size)
                pbuff = buffx

                bufflen = 0
    if pbuff is not None:
        bufflen, bank, size = binformat(bufflen, bank, outf, size)
    # write exit code

    if bank == 0:
        # if last raw statement unfinished, finish it with terminator zero.
        outf.write("10x0\n")
        size += 1
    else:
        # else, finish it with blank null as terminator.
        outf.write("null\n")
        size += 1
    outf.close()
    print("Done.")
    print(g2com.nonetformatted_smart(size))
    return


def binformat(bufflen, bank, outf, size):
    splitup = True
    bufflen += 1
    start = True
    while splitup:
        # DO NOT USE 9841! it will integer-overflow the BINRLE module's decoder
        # algorithm!
        if bufflen > 9041:
            bufflen -= 9041
            if start:
                presetval = "9041"
                start = 0
            else:
                presetval = "-9041"
            if bank == 1:
                bank = 0
                outf.write("raw;10x" + presetval + ",")
            else:
                bank = 1
                outf.write("10x" + presetval + "\n")
                size += 1

            if bufflen <= 9841 and bufflen > 0:
                splitup = False
                if bank == 1:
                    bank = 0
                    outf.write("raw;10x" + str(-bufflen) + ",")
                else:
                    bank = 1
                    outf.write("10x" + str(-bufflen) + "\n")

        elif bufflen > 0:
            splitup = False
            if bank == 1:
                bank = 0
                outf.write("raw;10x" + str(bufflen) + ",")
            else:
                bank = 1
                outf.write("10x" + str(bufflen) + "\n")
                size += 1
            bufflen = 0
        if bufflen <= 0:
            splitup = False
    return bufflen, bank, size


def binencode(rgb, offset=0):
    r = rgb[0] + offset
    g = rgb[1] + offset
    b = rgb[2] + offset
    mono = (r + g + b) / 3.0
    if mono > 127:
        return 1
    else:
        return 0


def plot_RLE(imagepath, lineinterpol=0, threshold=None):
    print("converting image into PLRLE plotter image format...")
    if threshold is not None:
        try:
            threshold = int(threshold)
        except ValueError:
            sys.exit("INVALID THRESHOLD ARGUMENT!")
        if threshold < 0:
            sys.exit("INVALID THRESHOLD ARGUMENT!")
    image = pygame.image.load(imagepath)
    xsize = image.get_width()
    ysize = image.get_height()
    pixcol = None
    # print(image.get_height())
    # print(ysize)
    size = 1
    pbuff = None
    bufflen = 0
    outf = open(imagepath.rsplit(".")[0] + ".tas0", 'w')
    outf.write('''#SBTCVM Gen2-9 GFXCON: run-length encoded tritmap
#Needs to be decoded manually.
#image file: ''' + imagepath + "\n"
               '''null;>.DATASIZE
''')
    for coly in xrange(0, ysize):
        buffx = ""
        for linex in xrange(0, xsize):
            prevpix = pixcol
            pixcol = image.get_at((linex, coly))
            if threshold is not None and prevpix is not None:
                if abs(
                    prevpix[0] -
                    pixcol[0]) < threshold and abs(
                    prevpix[1] -
                    pixcol[1]) < threshold and abs(
                    prevpix[2] -
                        pixcol[2]) < threshold:
                    pixcol = prevpix
            if lineinterpol == 0:
                buffx = bin8totrit3(
                    pixcol[0]) + bin8totrit3(pixcol[1]) + bin8totrit3(pixcol[2])
            else:
                if coly % 2:
                    buffx = bin8totrit3(
                        pixcol[0] - 5) + bin8totrit3(pixcol[1] - 5) + bin8totrit3(pixcol[2] - 5)
                else:
                    buffx = bin8totrit3(
                        pixcol[0]) + bin8totrit3(pixcol[1]) + bin8totrit3(pixcol[2])
            if buffx == pbuff:
                bufflen += 1
                buffx = ""
            elif pbuff is None:
                pbuff = buffx
                buffx = ""
                size += 1
                bufflen = 0
            else:
                outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
                pbuff = buffx
                buffx = ""
                size += 1
                bufflen = 0
        if pbuff is not None:
            outf.write("raw;10x" + str(bufflen) + "," + pbuff + "\n")
        pbuff = None
        buffx = ""
        size += 1
        bufflen = 0
        outf.write("raw;-,0\n")
        outf.write("###LINE DIV\n")
        # print(coly)
    outf.write("null;;.DATASIZE\n")
    outf.close()
    print("Done.")
    print(g2com.nonetformatted_smart(size))
    return


def bin8totrit3(level):
    if level < 0:
        level = 0
    if level > 255:
        level = 255
    # print(level)
    xtemp = btint(int(level / 9.44444444) - 13)
    # print(xtemp.intval)
    xtemp.changeval(xtemp.dectrunk(3))
    return xtemp.bttrunk(3)


if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
    except IndexError:
        cmd = None
    try:
        arg = sys.argv[2]
    except IndexError:
        arg = None
    try:
        arg2 = sys.argv[3]
    except IndexError:
        arg2 = None
    if cmd in ["-h", "--help"]:
        print('''SBTCVM Gen2-9 gfx conversion utility.
-p(n) [image]     : convert an image into 3-color ternary-packed art,
	and place it in a tas0 file. append n for no trailing newline.
-cp(n) [image]    : convert an image into 27-color ternary packed art,
	and place it in a tas0 file. append n for no trailing newline.
-cprle(n) [image] : convert an image into 27-color cprle compressed
	packed art image data.
-plrle(i) [image] (threshold) : convert an image into 9-trit (PLRLE format) rle compressed.
	tritmap image. append i for line-based striped interpolation.
	follow image name by an OPTIONAL threshold integer value a color channel must change for encoder to change colors.
	(at cost of detail)
-binrle [image] : boolean (2 tone) RLE-compressed tritmap format. uses BINRLE module.
-binrlei [image] : same as -binrle, only enable 2-line interpolation.
-binrlei4 [image] : same as -binrle, only enable 4-line interpolation.''')
    elif cmd in ["-v", "--version"]:
        print(
            "SBTCVM Gen2-9 gfx conversion utility. v1.0.0\n" +
            "part of SBTCVM-Gen2-9 v2.1.0.alpha")
    elif cmd in ["-a", "--about"]:
        print('''SBTCVM Gen2-9 gfx conversion utility.
v1.0.0
part of SBTCVM-Gen2-9 (v2.1.0.alpha)

Copyright (c) 2016-2022 Thomas Leathers and Contributors

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
        packart_maker(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1))

    elif cmd in ["-cp"]:
        print("Color Ternary-Packed art encoder.")
        colart_maker(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1))
    elif cmd in ["-pn"]:
        print("Ternary-Packed art encoder.")
        packart_maker(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            1)

    elif cmd in ["-cpn"]:
        print("Color Ternary-Packed art encoder.")
        colart_maker(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            1)

    elif cmd in ["-cprle"]:
        print("Color Ternary-Packed art encoder (RLE compressed).")
        colart_maker_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1))
    elif cmd in ["-cprlen"]:
        print("Color Ternary-Packed art encoder (RLE compressed).")
        colart_maker_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            1)
    elif cmd in ["-plrle"]:
        print("RLE-encoded 9-trit RGB tritmap.")
        plot_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            lineinterpol=0,
            threshold=arg2)
    elif cmd in ["-plrlei"]:
        print("RLE-encoded 9-trit RGB tritmap. (line interpolated)")
        plot_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            lineinterpol=1,
            threshold=arg2)
    elif cmd in ["-binrle"]:
        print("RLE-encoded boolean tritmap.")
        plot_BIN_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            lineinterpol=0)
    elif cmd in ["-binrlei"]:
        print("RLE-encoded boolean tritmap. (line interpolated)")
        plot_BIN_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            lineinterpol=1)
    elif cmd in ["-binrlei4"]:
        print("RLE-encoded boolean tritmap. (4 line interpolated)")
        plot_BIN_RLE(
            iofuncts.findtrom(
                arg,
                ext=".png",
                exitonfail=1,
                exitmsg="image file was not found. STOP",
                dirauto=1),
            lineinterpol=2)

    elif cmd is None:
        print("Tip: try gfxcon.py -h for help.")
    elif cmd.startswith("-"):
        print("Unknown option: '" + cmd + "' try gfxcon.py -h for help.")
