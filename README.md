image-nikon-format
==================

Nikon image filename formatting based on date and time


Description
-----------

This program restructure Nikon NEF and JPG files 
based on date, time and subsec. No 2 files can have
the same name.

while renaming, it still checks if the destination 
file exists; it does not overwrite an existing file
in the process of rename. It simply skips.


Files
-----

```
exif.py
nikon.py
index.py   : nikon dslr photo formatting

vindex.py  :
mindex.py  :
p900.py    : p900 photo formatting
dashcam.py : dashcam video formatting
```

Disclaimer
----------

It is based on exif.py which has been borrowed from 
open source. The credit for exif.py goes to the 
writers of that file.


Copyright
---------

Author: Snehasis Sinha, 2016

This program is open source. Anyone can use, modify
this program without any permission. This program
comes without any waranty and terms of use. Author
will not be responsible for any damage etc.
