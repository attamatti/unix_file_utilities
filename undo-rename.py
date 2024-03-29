#!/usr/bin/python

# use the RENAME.log file generated by rename.py to roll back the changes made by the script.

import sys
import os
import datetime
vers = 0.1


rendata = open('RENAME.log','r').readlines()
splits = []
for i in rendata[1:]:
    if "rename utility" in i or "remove-filename-bits" in i:
        splits.append((i.replace('\n',''),rendata.index(i)))
splits.append(('last',len(rendata)))

splitchoices = {}
n = 1
if len(splits) > 2:
    print "\n** multiple runs of rename.py detected **"
    for i in splits:
        if i[0] != 'last':
            print "{0}) {1}".format(n,i[0].split(' - ')[-1])
            splitchoices[n] = i
            n+=1
    splitchoices[n] = splits[-1] 
    which = int(raw_input('which one to use: '))

commandlist = []
skip = []
if len(splits) > 2:
    runon = rendata[(splitchoices[which][1])+1:splitchoices[which+1][1]]
else:
    runon = rendata[2:]
    
for i in runon:
    currfile = i.split(' --> ')[1].replace('\n','')
    originalfile = i.split(' --> ')[0]
    if os.path.isfile(currfile) == True:
        commandlist.append('mv {0} {1}'.format(currfile,originalfile))
    else:
        skip.append("file {0} not found -- skipping".format(currfile))

print "\nCommands to run: "
for i in commandlist:
    print i
if len(skip) > 0:
    for i in skip:
        print i
    print "{0} files skipped".format(len(skip))
print "{0} files to operate on".format(len(commandlist))

doit = raw_input('do it (y/n)? ')
if doit not in ['y','Y','Yes','YES','yes']:
    sys.exit('User quit - Goodbye')
    
output = open('RENAME.log','a')
output.write('\nrename utility ** UNDO ** vers {0} - {1}'.format(vers,datetime.datetime.now()))
for i in commandlist:
    os.system(i)
    outwrite = i.split()[1]+' --> '+i.split()[2]
    output.write('\n{0}'.format(outwrite))
