#!env python

import os
import sys
import getopt

class xtool:
	cmd = 'mdls'
	parameter = 'kMDItemFSContentChangeDate'
	obj = {}
	ext = 'MOV'

	def __init__ (self, args):
		self.obj['oldbase'] = args.get('file').replace ("." + self.ext, "")
		 
	
	def toyear ( self, year ):
		return '%1s' % chr(int(year)-2011 + ord('A'))

	def tomonth ( self, month ):
		return '%1X' % int(month)
		
	def extract (self):
		out = os.popen (self.cmd + " " + self.obj['oldbase']+"."+self.ext).read()
		tmp = ""
		for line in out.split ("\n"):
		 	if (line.startswith (self.parameter)):
				tmp = line
				break
		
		junk,value = tmp.split ("= ", 1)
		dt, tm, tz = value.split (" ")
		# print "date=[" + dt + "] time=[" + tm + "]"
		y,m,d = dt.split ("-")
		dt = "%s%s%02d" % (self.toyear (y), self.tomonth (m), int(d))
		
		#b = tm
		#b = b.replace (":", "")
		tm = tm.replace (":", "")
		#b = b.replace (" ", "_")

		self.obj['newbase'] = dt + "_" + tm
		return self
	
	def convert (self, too, confirm=False, msg=''):
		if confirm:
			os.rename ( self.obj['oldbase']+"."+too.upper(), self.obj['newbase']+"."+too.upper() )
		print '%-15s %-25s %s' % ( self.obj['oldbase']+"."+too.upper(), self.obj['newbase']+"."+too.upper() , msg)

	def exists (self, arg):
		return {
			'newfile' : os.path.exists (self.obj['newbase'] + "." + self.ext),
			}.get (arg, False)


def main (progname, argv):
	prefix = 'DSC'
	suffix = 'MOV'
	change = False
	opts   = None

	try:
		opts, args = getopt.getopt (argv, "c", ['change'])
	except getopt.GetoptError:
		print progname + ' --change <files>'
		sys.exit (1)

	for opt, arg in opts:
		if opt in ('--change'): change = True

	for arg in args:
		if arg.endswith (".MOV"):
			x = xtool ( {'file': arg} ).extract()
			if not x.exists ('newfile'):
				x.convert ('mov', change)
			else:
				x.convert('mov', False, '__skipped__')

		
if __name__ == '__main__':
	main (sys.argv[0], sys.argv[1:])
