#!/usr/bin/python

# remove bits from a filename

import sys
import glob
import os
import datetime

vers = "0.1"

files = glob.glob(raw_input('file search string: ') or '*.ext')
for i in files:
    print i
print '{0} files'.format(len(files))

print "1) remove/replace specific bit from all file names"
print "2) remove n characters from the front or back of file names"
select = raw_input("which: ")

commandlist = []

if select == '1':
    bit = raw_input('bit to remove/replace: ')
    s=raw_input('Replace with what? (leave blank to remove: )') or ''
    for i in files:
        namelist = i.split(bit)
        newname = s.join(namelist)
        commandlist.append("mv {0} {1}".format(i,newname))

elif select == '2':
    n = int(raw_input('number of characters to remove: '))
    print "1) from front"
    print "2) from back (leaves the extension intact)"
    fob = raw_input('which: ')
    
    if fob == '1':
        for i in files:
            newname = i[n:]
            commandlist.append('mv {0} {1}'.format(i,newname))
    if fob == '2':
        for i in files:
            filesplit = i.split('.')
            newname = filesplit[0][:-n]+'.'+filesplit[1]
            commandlist.append('mv {0} {1}'.format(i,newname))
else:
    sys.exit('not an option - goodbye')

for i in commandlist:
    print i


doit = raw_input('do it (y/n) ? ')
if doit not in ['y','Y','Yes','YES','yes']:
    sys.exit("User quit: Goodbye")
else:
    logfile = open("REMOVEBITS.log","a")
    logfile.write("\nremove-filename-bits.py vers {0} - {1}".format(vers,datetime.datetime.now()))
    for i in commandlist:
        os.system(i)
        logfile.write('\n{0}'.format(i))