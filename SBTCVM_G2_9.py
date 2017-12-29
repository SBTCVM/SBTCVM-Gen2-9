#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.MEM_G2x_9
import VMSYSTEM.CPU_G2x_9

memsys=VMSYSTEM.MEM_G2x_9.memory("TESTSHORT.TROM")
#Test Memory system.
#data R/W
print memsys.getdata(libbaltcalc.mni(9))
memsys.setdata(libbaltcalc.mni(9), btint(12))
print memsys.getdata(libbaltcalc.mni(9))
#instruction R/W
print memsys.getinst(libbaltcalc.mni(9))
memsys.setinst(libbaltcalc.mni(9), btint(13))
print memsys.getinst(libbaltcalc.mni(9))