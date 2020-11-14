#!/usr/bin/env python

#v3.2.0

def numflip(numtoflip):
	return(numtoflip[::-1])

#converts balanced ternary integers to decimal.
#this is a core function to the library.
def BTTODEC(NUMTOCONV1):
	FLIPPEDSTR1=(numflip(NUMTOCONV1))
	EXTRAP1=0
	SUMDEC1=0
	for btnumlst1 in FLIPPEDSTR1:
		EXTPOLL1 = (3**EXTRAP1)
		if btnumlst1==("+"):
			SUMDEC1 += EXTPOLL1
		if btnumlst1==("-"):
			SUMDEC1 -= EXTPOLL1
		EXTRAP1 += 1
	return (SUMDEC1)

#converts decimal integers to balanced ternary.
#this is a core function to the library.
def DECTOBT(NUMTOCONV1):
	digbat=""
	while NUMTOCONV1 != 0:
		if NUMTOCONV1 % 3 == 0:
			#note_digit(0)
			digbat=("0" + digbat)
		elif NUMTOCONV1 % 3 == 1:
			#note_digit(1)
			digbat=("+" + digbat)
		elif NUMTOCONV1 % 3 == 2:
			#note_digit(-1)
			digbat=("-" + digbat)
		NUMTOCONV1 = (NUMTOCONV1 + 1) // 3
	#print NUMTOCONV1
	#zero exception
	if (str(digbat)==""):
		digbat="0"
	return(digbat)



def tritchop(decimal_int, split_point):
	tritcount=0
	retlist=[]
	issplit=False
	for f in [0, 0]:
		while decimal_int != 0:
			if decimal_int % 3 == 0:
				#0
				pass
			elif decimal_int % 3 == 1:
				#+
				f+=(3**tritcount)
			elif decimal_int % 3 == 2:
				#-
				f-=(3**tritcount)
			tritcount+=1
			decimal_int = (decimal_int + 1) // 3
			if tritcount==split_point and not issplit:
				tritcount=0
				issplit=True
				break
		retlist.append(f)
	return retlist

def tritmerge(decimal_int_upper, decimal_int_lower, length_of_lower):
	return ((decimal_int_upper * (3**length_of_lower)) + decimal_int_lower)

def btmul(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon * numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

def btadd(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon + numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

def btsub(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon - numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

#note that values may not be exact. this is due to that the libbaltcalc currently handles integers only.

def btdivcpu(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	try:
		decRes=(numAcon // numBcon)
	except ZeroDivisionError:
		#Special zero divisoon return for SBTCVM to detect. "ZDIV"
		return "ZDIV"
	btRes=(DECTOBT(decRes))
	return(btRes)
	
def btdiv(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon // numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)
btdev=btdiv

def mpi(tritlen):
	return (((3**(tritlen))-1)//2)
def mni(tritlen):
	return ( - ((3**(tritlen))-1)//2)
def mcv(tritlen):
	return (3**(tritlen))
	


#inverts the positive and negative numerals in a balanced ternary integer, 
#(ie +-0- would become -+0+ and vice versa)
def BTINVERT(numtoinvert):
	BTINV1 = numtoinvert.replace("-", "P").replace("+", "-").replace("P", "+")
	#print BTINV2
	return (BTINV1)

def trailzerostrip(numtostri):
	pritokfg=0
	#print ("argh -.-" + numtostri)
	numtostri = numtostri.replace("-", "T").replace("+", "1")
	#numtostri = (numflip(numtostri))
	numretbankd=""
	#print (numtostri)
	allzero=1
	for fnumt in numtostri:
		if (fnumt=="T" or fnumt=="1"):
			pritokfg=1
			allzero=0
		if pritokfg==1:
			numretbankd = (numretbankd + fnumt)
		if pritokfg==0:
			nullbox=fnumt
		#print (fnumt)
	if allzero==1:
		numretbankd="0"
	numretbankd = numretbankd
	#print (numretbankd.replace("T", "-").replace("1", "+"))
	return (numretbankd.replace("T", "-").replace("1", "+"))


# a "programmable" biased and gate. returns a positive if:
#input a (inpA) = input b (inpB) = polarity line (polarset)
#else it returns zero
def progbiasand(polarset, inpA, inpB):
	if (inpA==polarset and inpB==polarset):
		return("+")
	elif (inpA!=polarset or inpB!=polarset):
		return("0")
#a polarized and gate
#returns + if both input A (inpA) and input B (inpB) = + 
#returns - if both input A (inpA) and input B (inpB) = -
#otherwise it returns zero
def polarityand(inpA, inpB):
	if (inpA=="+" and inpB=="+"):
		return("+")
	elif (inpA=="-" and inpB=="-"):
		return("-")
	elif (inpA!="+" or inpB!="+"):
		return("0")
	elif (inpA!="-" or inpB!="-"):
		return("0")

# a programmable biased or gate returns "+" if either or both inputs equal the pollarity line (polarset)
#else it returns "0"
def progbiasor(polarset, inpA, inpB):
	if (inpA==polarset or inpB==polarset):
		return("+")
	elif (inpA!=polarset or inpB!=polarset):
		return("0")
# a programmable biased orn gate returns "+" if either  equal the pollarity line (polarset)
#returns "0" either if neither or both inputs equal the pollarity line (polarset)
def progbiasnor(polarset, inpA, inpB):
	if (inpA==polarset and inpB==polarset):
		return("0")
	elif (inpA!=polarset and inpB==polarset):
		return("+")
	elif (inpA==polarset and inpB!=polarset):
		return("+")
	elif (inpA!=polarset and inpB!=polarset):
		return("0")

#trit truncation helper for btint.bttrunk method.
def trunkhelper(tritlen, decint):
	#(('0'*tritlen) + DECTOBT(self.intval))[:tritlen]
	btstr=DECTOBT(decint)
	if len(btstr)<tritlen:
		return (('0' * (tritlen - len(btstr))) + btstr)
	else:
		return btstr[-tritlen:]

def dectrunkhelper(tritlen, decint):
	mpival=mpi(tritlen)
	if decint<-mpival:
		return -mpival
	elif decint>mpival:
		return mpival
	else:
		return decint

class btint(object):
	__slots__ = ('intval')
	def __init__(self, stringint):
		#store integer in signed decimal integer.
		if type(stringint) is int:
			self.intval=stringint
		else:
			try:
				self.intval=stringint.intval
			except AttributeError:
				self.intval=BTTODEC(str(stringint).replace("p", "+").replace("n", "-"))
	def __str__(self):
		return DECTOBT(self.intval)
	def __int__(self):
		return self.intval
	def dec(self):
		return self.intval
	def bt(self):
		return DECTOBT(self.intval)
	def p0n(self):
		return (DECTOBT(self.intval).replace("+", "p").replace("-", "n"))
	def copy(self):
		return btint(self.intval)
	def changeval(self, newval):
		if type(newval) is int:
			self.intval=newval
		else:
			try:
				self.intval=newval.intval
			except AttributeError:
				self.intval=BTTODEC(str(newval).replace("p", "+").replace("n", "-"))
	#addition
	def __add__(self, other):
		if isinstance(other, btint):
			return btint((self.intval + other.intval))
		elif isinstance(other, int):
			return btint((self.intval + other))
		else:
			return NotImplemented
	def __radd__(self, other):
		if isinstance(other, int):
			return btint((other + self.intval))
		else:
			return NotImplemented
	def __iadd__(self, other):
		if isinstance(other, btint):
			self.intval += other.intval
			return self
		elif isinstance(other, int):
			self.intval += other
			return self
		else:
			return NotImplemented
	#subtraction
	def __sub__(self, other):
		if isinstance(other, btint):
			return btint((self.intval - other.intval))
		elif isinstance(other, int):
			return btint((self.intval - other))
		else:
			return NotImplemented
	def __rsub__(self, other):
		if isinstance(other, int):
			return btint((other - self.intval))
		else:
			return NotImplemented
	def __isub__(self, other):
		if isinstance(other, btint):
			self.intval -= other.intval
			return self
		elif isinstance(other, int):
			self.intval -= other
			return self
		else:
			return NotImplemented
	#division
	def __floordiv__(self, other):
		if isinstance(other, btint):
			return btint((self.intval // other.intval))
		elif isinstance(other, int):
			return btint((self.intval // other))
		else:
			return NotImplemented
	def __rfloordiv__(self, other):
		if isinstance(other, int):
			return btint((other // self.intval))
		else:
			return NotImplemented
	def __ifloordiv__(self, other):
		if isinstance(other, btint):
			self.intval //= other.intval
			return self
		elif isinstance(other, int):
			self.intval //= other
			return self
		else:
			return NotImplemented
	#multiplication
	def __mul__(self, other):
		if isinstance(other, btint):
			return btint((self.intval * other.intval))
		elif isinstance(other, int):
			return btint((self.intval * other))
		else:
			return NotImplemented
	def __rmul__(self, other):
		if isinstance(other, int):
			return btint((other * self.intval))
		else:
			return NotImplemented
	def __imul__(self, other):
		if isinstance(other, btint):
			self.intval *= other.intval
			return self
		elif isinstance(other, int):
			self.intval *= other
			return self
		else:
			return NotImplemented
	#compare
	def __cmp__(self, other):
		if isinstance(other, btint):
			if self.intval<other.intval:
				return -1
			elif self.intval>other.intval:
				return 1
			else:
				return 0
		elif isinstance(other, int):
			if self.intval<other:
				return -1
			elif self.intval>other:
				return 1
			else:
				return 0
		else:
			return NotImplemented
	def __lt__(self, other):
		if isinstance(other, btint):
			return self.intval<other.intval
		elif isinstance(other, int):
			return self.intval<other
		else:
			return NotImplemented
	def __le__(self, other):
		if isinstance(other, btint):
			return self.intval<=other.intval
		elif isinstance(other, int):
			return self.intval<=other
		else:
			return NotImplemented
	def __gt__(self, other):
		if isinstance(other, btint):
			return self.intval>other.intval
		elif isinstance(other, int):
			return self.intval>other
		else:
			return NotImplemented
	def __ge__(self, other):
		if isinstance(other, btint):
			return self.intval>=other.intval
		elif isinstance(other, int):
			return self.intval>=other
		else:
			return NotImplemented
	def __ne__(self, other):
		if isinstance(other, btint):
			return self.intval!=other.intval
		elif isinstance(other, int):
			return self.intval!=other
		else:
			return NotImplemented
	def __eq__(self, other):
		if isinstance(other, btint):
			return self.intval==other.intval
		elif isinstance(other, int):
			return self.intval==other
		else:
			return NotImplemented
	#length (measured in trits)
	def __len__(self):
		return len(DECTOBT(self.intval))
	#others
	def __abs__(self):
		return btint(abs(self.intval))
	def __neg__(self):
		return btint( - self.intval)
	def __pos__(self):
		return btint( + self.intval)
	def __invert__(self):
		return btint( - self.intval)
	def invert(self):
		return btint( - self.intval)
	#truncation
	def bttrunk(self, tritlen):
		return trunkhelper(tritlen, self.intval)
	def dectrunk(self, tritlen):
		return btint(dectrunkhelper(tritlen, self.intval))
		