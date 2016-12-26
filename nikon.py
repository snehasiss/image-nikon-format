import exif
import os

class nikon:
	files = []
	def __init__ (self, args):
		prefix      = args.get('prefix') or 'DSC'
		self.suffix = args.get('suffix') or 'NEF'
		self.change = args.get('change') or False

		files = os.listdir ( os.getcwd() )
		for f in files:
			if f.endswith (self.suffix) and f.startswith (prefix):
				self.files.append (f)

	def format (self, datestr):
		year, month, day  = datestr.get('date').split (':')
		hour, minute, sec = datestr.get('time').split (':')
		subsec = datestr.get('subsec')

		self.code = '%04s%02s%02s-%02s%02s%02s.%02s' % (year, month, day, hour, minute, sec, subsec)

		# date format
		year  = '%1s' %  chr ( int(year) - 2011 + ord ('A') )
		month = '%1X' % int (month)
		day   = '%02d' % int (day)

		# hour format
		hour   = int (hour)
		hour = '%1s' % chr ( hour + ord ('A') )

		# min, sec, subsec format in hex
		time = int (minute) * 600 + int (sec) * 10 + int(subsec)/10  
		time = '%04X' % time

		# new format for time introduced here 
		number = list (time)
		i = 0
		for d in number:
			x = int ( d, 16 )
			e = chr ( x + ord ('A') )
			number[i] = '%1s' % e
			i = i + 1

		time = ''.join (number)
		# new format of time ends

		self.newname = year + month + day + '_' + hour + time + '.' + self.suffix

	def parse (self, filename):
		self.filename = filename
		keys = ['EXIF DateTimeOriginal', 'EXIF SubSecTimeOriginal']

		with open (filename, 'rb') as f:
			data = exif.process_file (f, stop_tag='UNDEF', details=False, strict=False, debug=False)
		
		#for key in keys:
		#	print " %s: %s" %  (key, data[key].printable)

		dateraw = data[ keys[0] ].printable
		date, time = dateraw.split (' ')
		subsec = data[ keys[1] ].printable
	
		self.format ( { 'date': date, 'time': time, 'subsec': subsec } )

	def process (self):
		for filename in self.files:
			self.parse (filename)
			out = '%20s  %-14s  %13s' % ( self.code, self.filename, self.newname )
			if self.change:
				if os.path.isfile (self.newname):
					out = out + '  __SKIPPED__'
				else:
					out = out + '  OK'
					os.rename (self.filename, self.newname)
			print out
			

# end nikon #
