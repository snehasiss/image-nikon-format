import exif
import os

class nikon:
	files = []
	skipped = {}

	def __init__ (self, args):
		prefix      = args.get('prefix') or 'DSC'
		self.suffix = args.get('suffix') or 'NEF'
		self.change = args.get('change') or False

		files = os.listdir ( os.getcwd() )
		for f in files:
			if f.endswith (self.suffix) and f.startswith (prefix):
				self.files.append (f)

	def toyear (self, year):
		year  = int(year) - 2000
		if year < 10:
			year = '1%s' % year
		else:
			year  = '%1s' %  chr ( year - 10 + ord ('A') )

		return year

	def tomonth (self, month):
		month = '%1X' % int (month)
		return month

	def today (self, day):
		day   = '%02d' % int (day)
		return day

	def tohour (self, hour):
		hour   = int (hour)
		#hour = '%1s' % chr ( hour + ord ('A') )
		hour = '%02d' % hour
		return hour

	def totime (self, minute, second):
		# time = '%02s%02s%1s' % (minute, second, int (subsec) / 10)
		# time = '%02s%02s_%1s' % (minute, second, int (subsec) / 10)
		time = '%02s%02s' % (minute, second)
		return time

	def format (self, datestr):
		year, month, day  = datestr.get('date').split (':')
		hour, minute, sec = datestr.get('time').split (':')
		subsec = datestr.get('subsec')

		self.code = '%04s-%02s-%02s-%02s-%02s-%02s-%02s' % (year, month, day, hour, minute, sec, subsec)
		#self.newname = self.toyear (year) + self.tomonth (month) + self.today (day) + self.tohour (hour) + '_' + self.totime (minute, sec, subsec) + '.' + self.suffix
		#print "subset: " + subsec 

		self.idx = '%1s' % (int (subsec) / 10)
		#print "index: " + self.idx

		self.newbase = self.toyear (year) + self.tomonth (month) + self.today (day) + '_' + self.tohour (hour) + self.totime (minute, sec)
		self.newname = self.newbase + '_' + self.idx + '.' + self.suffix.upper()

	def get_next_idx (self, a):
		v = ord (a)

		if v >= ord ('0') and v <= ord ('9'):
			v = ord ('A')
		else:
			v = v + 1

		return '%1s' % (chr(v))

	def getnext (self):
		self.idx = self.get_next_idx (self.idx)
		self.newname = self.newbase + '_' + self.idx + '.' + self.suffix.upper()

	def parse (self, filename):
		self.filename = filename
		keys = ['EXIF DateTimeOriginal', 'EXIF SubSecTimeOriginal']

		with open (filename, 'rb') as f:
			data = exif.process_file (f, stop_tag='UNDEF', details=False, strict=False, debug=False)
		

		dateraw = data[ keys[0] ].printable
		date, time = dateraw.split (' ')
		subsec = data[ keys[1] ].printable
	
		self.format ( { 'date': date, 'time': time, 'subsec': subsec } )

	def process (self):
		for filename in self.files:
			try:
				self.parse (filename)
			except KeyError:
				print '%20s  %-18s  __failed__' % ( self.code, self.filename )
				continue

			if (self.filename == self.newname):
				print '%20s  %-18s  __skipped_' % ( self.code, self.filename )
				continue
	
			while ( os.path.isfile (self.newname) ):
				self.getnext()

			out = '%20s  %-18s  %-20s' % ( self.code, self.filename, self.newname )
			if self.change:
				os.rename (self.filename, self.newname)
			print out
			

# end nikon #
