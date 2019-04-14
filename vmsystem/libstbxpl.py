#!/usr/bin/env python


compvers='v0.1.0'
versint=(0, 1, 0)

#SBTCVM Ternary Blocked eXstensible Programming Language
#'c-ish' programming language for SBTCVM Gen2-9

Default_children={}
GlobalVariableList={}

class codeblock:
	def __init__(self, fileobj, filename, head, contents, parent=None, allowed_children=Default_children):
		self.alow_childs=allowed_children.copy()
		self.fobj=filename
		self.contents=contents
		self.fname=filename
		self.children={}
		self.head=head
	def parse(self):
		incomment=0
		instring=0
		inhead=1
		inchild=0
		#commentx=""
		pchar=None
		#per-character parser engine
		for charlist in self.contents:
			nchar=charlist[0]
			#comment handler code.
			if nchar=="*" and pchar=="/" and inhead==1 and instring==0 and inchild==0:
				incomment=1
				#commentx=""
			elif nchar=="/" and pchar=="*" and incomment==1:
				incomment=0
				#print("Comment: '" + commentx + "'")
				nchar=None
			elif incomment==1:
				#commentx=commentx+nchar
				pass
				
			#always set pchar to value of nchar at end of main for loop.
			pchar=nchar
		
def parse(filename):
	fileobj=open(filename, "r")
	content=[]
	lineno=0
	for line in fileobj:
		lineno+=1
		colno=0
		for char in line:
			colno+=1
			content.append([char, filename, lineno, colno])
		
	initblock=codeblock(fileobj,filename, "global", content, parent=None, allowed_children=Default_children)
	initblock.parse()
