#!/usr/bin/env python



def inttob9(intval):
	remainder = int(intval)
	output=""
	while remainder!=0:
		#print(remainder)
		chunk, remainder = b9chop(remainder, 1)
		#print(str(remainder) + " " + str(chunk))
		output=ditrit_b9_dict[chunk] + output
	
	if output=="":
		return "0"
	return output
def b9toint(base9_string):
	total=0
	for i in base9_string:
		ditrit=b9_ditrit_dict[i]
		total=b9merge(total, ditrit, 1)
	return total

b9_ditrit_dict={
"4": +4,
"3": +3,
"2": +2,
"1": +1,
"0":  0,
"Z": -1,
"Y": -2,
"X": -3,
"W": -4}

ditrit_b9_dict={}
for f in b9_ditrit_dict:
	ditrit_b9_dict[b9_ditrit_dict[f]]=f

def b9chop(decimal_int, split_point):
	split_point=split_point*2
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

def b9merge(decimal_int_upper, decimal_int_lower, length_of_lower):
	length_of_lower=length_of_lower*2
	return ((decimal_int_upper * (3**length_of_lower)) + decimal_int_lower)

