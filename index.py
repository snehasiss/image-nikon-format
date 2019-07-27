import nikon
import sys
import getopt

def main (progname, argv):
	prefix = 'DSC'
	suffix = 'NEF'
	change = False
	opts   = None

	try:
		opts, args = getopt.getopt (argv, "p:s:c", ['prefix=', 'suffix=', 'change'])
	except getopt.GetoptError:
		print progname + ' --prefix PREFIX --suffix SUFFIX --change'
		sys.exit (1)

	for opt, arg in opts:
		if opt in ('--prefix'): prefix = arg
		elif opt in ('--suffix'): suffix = arg
		elif opt in ('--change'): change = True

	if not suffix in ('NEF', 'nef', 'JPG', 'jpg'):
		print 'supported file type: NEF, JPG'
		sys.exit (2)

	params = { 'prefix': prefix, 'suffix': suffix, 'change': change }
	n = nikon.nikon (params)
	n.process ()
	
		
if __name__ == '__main__':
	main (sys.argv[0], sys.argv[1:])
