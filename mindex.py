#!env python

import os
import sys

class xtool:
	cmd = 'exiftool'
	obj = {}
	ext = 'MOV'

	def __init__ (self, args):
		self.obj['oldbase'] = args.get('file').replace ("." + self.ext, "")
		 
	
	def toyear ( self, year ):
		return '%1s' % chr(int(year)-2011 + ord('A'))

	def tomonth ( self, month ):
		return '%1x' % int(month)
		
	def extract (self):
		out = os.popen (self.cmd + " " + self.obj['oldbase']+"."+self.ext).read()
		tmp = ""
		for line in out.split ("\n"):
		 	if (line.startswith ("Create Date")):
				tmp = line
				break
		
		junk,value = tmp.split (": ", 1)
		dt, tm = value.split (" ")
		print "date=[" + dt + "] time=[" + tm + "]"
		y,m,d = dt.split (":")
		dt = "%s%s%02d" % (self.toyear (y), self.tomonth (m), int(d))
		print dt
		
		b = value
		b = b.replace (":", "")
		b = b.replace (" ", "_")

		self.obj['newbase'] = "TS" + b
		return self
	
	def convert (self, too, confirm=False):
		if confirm:
			os.rename ( self.obj['oldbase']+"."+too.upper(), self.obj['newbase']+"."+too.upper() )
		print '%-15s %-25s' % ( self.obj['oldbase']+"."+too.upper(), self.obj['newbase']+"."+too.upper() )

	def exists (self, arg):
		return {
			'newfile' : os.path.exists (self.obj['newbase'] + "." + self.ext),
			}.get (arg, False)


def main (args):
	confirm = False #True
	for arg in args:
		if arg.endswith (".MOV"):
			x = xtool ( {'file': arg} ).extract()
			if not x.exists ('newfile'):
				x.convert ('mov', confirm)

			if x.exists ('oldnmea') and not x.exists ('newnmea'):
				x.convert ('nmea', confirm)
			

if __name__ == '__main__':
	main (sys.argv[1:])
