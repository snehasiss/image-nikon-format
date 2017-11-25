#!env python

import os
import sys

class p900:
	cmd = 'exiftool'
	obj = {}

	def __init__ (self, args):
		self.obj['oldbase'], self.obj['extn'] = args.get('file').split ('.')
		 
	
	def toyear ( self, year ):
		return '%1s' % chr(int(year)-2011 + ord('A'))

	def tomonth ( self, month ):
		a = '%1x' % int(month)
		return a.upper()
		
	def extract (self):
		out = os.popen (self.cmd + " " + self.obj['oldbase']+"."+self.obj['extn']).read()
		tmp = ""
		for line in out.split ("\n"):
		 	if (line.startswith ("Create Date")):
				tmp = line
				break
		
		junk,value = tmp.split (": ", 1)
		dt, tm = value.split (" ")
		#print "date=[" + dt + "] time=[" + tm + "]"
		y,m,d = dt.split (":")
		dt = "%s%s%02d" % (self.toyear (y), self.tomonth (m), int(d))
		#print dt
		
		tm = tm.replace (":", "")

		self.obj['newbase'] = dt + '_' + tm
		return self
	
	def convert (self, confirm=False):
		if confirm:
			os.rename ( self.obj['oldbase'] + "." + self.obj['extn'], self.obj['newbase'] + "." + self.obj['extn'] )

	def callout (self, skip=False):
		skipmesg = ''
		if skip:
			skipmesg = '__skipped__'

		print '%-15s %-25s %s' % ( self.obj['oldbase'] + "." + self.obj['extn'], self.obj['newbase'] + "." + self.obj['extn'], skipmesg )

	def exists (self, arg):
		return {
			'newfile' : os.path.exists (self.obj['newbase'] + "." + self.obj['extn']),
			}.get (arg, False)


def main (args):
	confirm = True
	for arg in args:
		p = p900 ( {'file': arg} ).extract()
		if p.exists ('newfile'):
			p.callout (True)
			next

		p.convert (confirm)
		p.callout (False)


# main
if __name__ == '__main__':
	main (sys.argv[1:])
