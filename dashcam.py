#!env python

import os
import sys

class xtool:
	TCOMMAND  = 'mdls'
	PARAMETER = 'kMDItemFSContentChangeDate'

	# cmd = 'exiftool'
	cmd = TCOMMAND
	obj = {}

	def __init__ (self, args):
		self.obj['oldbase'] = args.get('file').replace (".MP4", "")
		 
	
	def extract (self):
		#
		# format: kMDItemFSContentChangeDate = 2018-07-07 14:32:46 +0000
		#
		out = os.popen (self.cmd + " " + self.obj['oldbase']+".MP4").read()
		tmp = ""
		for line in out.split ("\n"):
		 	if (line.startswith (self.PARAMETER)):
				tmp = line
				break
		
		left,right = tmp.split (" = ", 1)
		# right.lstrip(' ')
		dt,tm,tz   = right.split (" ", 2)
		dt = dt.replace ("-", "")
		tm = tm.replace (":", "")

		# a,b = tmp.split (":", 1)
		# b = b.replace (":", "")
		# b = b.replace (" ", "_")

		# self.obj['newbase'] = "TS" + b
		self.obj['newbase'] = "TS_" + dt + "_" + tm
		return self
	
	def convert (self, too, confirm=False):
		if confirm:
			os.rename ( self.obj['oldbase']+"."+too.upper(), self.obj['newbase']+"."+too.upper() )
		print '%-15s %-25s' % ( self.obj['oldbase']+"."+too.upper(), self.obj['newbase']+"."+too.upper() )

	def exists (self, arg):
		return {
			'newmp4' : os.path.exists (self.obj['newbase'] + ".MP4"),
			'oldnmea': os.path.exists (self.obj['oldbase'] + ".NMEA"),
			'newnmea': os.path.exists (self.obj['newbase'] + ".NMEA")
			}.get (arg, False)


def main (args):
	confirm = False
	for arg in args:
		if arg.endswith (".MP4"):
			x = xtool ( {'file': arg} ).extract()
			if not x.exists ('newmp4'):
				x.convert ('mp4', confirm)

			if x.exists ('oldnmea') and not x.exists ('newnmea'):
				x.convert ('nmea', confirm)
			

if __name__ == '__main__':
	main (sys.argv[1:])
