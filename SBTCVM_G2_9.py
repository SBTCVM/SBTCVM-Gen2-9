#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.MEM_G2x_9
import VMSYSTEM.CPU_G2x_9
import VMSYSTEM.IO_G2x_9

print "SBTCVM Generation 2 9-trit VM, v2.1.0.PRE-ALPHA\n"
#initalize memory subsystem
memsys=VMSYSTEM.MEM_G2x_9.memory("TESTSHORT.TROM")
#initalize IO subsystem
iosys=VMSYSTEM.IO_G2x_9.io()

cpusys=VMSYSTEM.CPU_G2x_9.cpu(memsys, iosys)


#preliminary Framework tests:

#Test Memory system.
#data R/W
print memsys.getdata(libbaltcalc.mni(9))
memsys.setdata(libbaltcalc.mni(9), btint(12))
print memsys.getdata(libbaltcalc.mni(9))
#instruction R/W
print memsys.getinst(libbaltcalc.mni(9))
memsys.setinst(libbaltcalc.mni(9), btint(13))
print memsys.getinst(libbaltcalc.mni(9))



#test IO
#dummy function to test IOSYS write notification.
def dummyfunct(addr, data):
	print "IOSYS NOTIFY TEST PASSED: IO ADDRESS:" + str(int(addr)) + " DATA:" + str(int(data))

#tell iosystem to call dummyfunct on write to address mni(9) (-9841)
iosys.setnotify(libbaltcalc.mni(9), dummyfunct)
print iosys.ioread(libbaltcalc.mni(9))
iosys.iowrite(libbaltcalc.mni(9), btint(12))
print iosys.ioread(libbaltcalc.mni(9))
