#!/usr/bin/env python



def inttob27(intval):
	remainder = int(intval)
	output=""
	while remainder!=0:
		#print(remainder)
		chunk, remainder = b27chop(remainder, 1)
		#print(str(remainder) + " " + str(chunk))
		output=triad_b27_dict[chunk] + output
	
	if output=="":
		return "0"
	return output
def b27toint(base27_string):
	total=0
	for i in base27_string:
		triad=b27_triad_dict[i]
		total=b27merge(total, triad, 1)
	return total

b27_triad_dict={"D": +13,
"C": +12,
"B": +11,
"A": 10,
"9": +9,
"8": +8,
"7": +7,
"6": +6,
"5": +5,
"4": +4,
"3": +3,
"2": +2,
"1": +1,
"0":  0,
"Z": -1,
"Y": -2,
"X": -3,
"W": -4,
"V": -5,
"U": -6,
"T": -7,
"S": -8,
"R": -9,
"Q": -10,
"P": -11,
"N": -12,
"M": -13}

triad_b27_dict={}
for f in b27_triad_dict:
	triad_b27_dict[b27_triad_dict[f]]=f

def b27chop(decimal_int, split_point):
	split_point=split_point*3
	tritcount=0
	retlist=[]
	issplit=False
	for f in [0, 0]:
		#print("--")
		while decimal_int != 0:
			#print(decimal_int)
			#
			#print(f)
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

def b27merge(decimal_int_upper, decimal_int_lower, length_of_lower):
	length_of_lower=length_of_lower*3
	return ((decimal_int_upper * (3**length_of_lower)) + decimal_int_lower)

