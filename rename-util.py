#!/usr/bin/python

vers = "1.3"

# general purpose utility for  renaming files.
# follow the prompts- should be self-explanitory 

# v1.1 improved template system for rename with original number 
# v1.2 fixed problem with sequential rename not being sorted properly
# v.13 changed * in file name template to & to avoid confusion

# Matt Iadanza 2015-01-25

#### imports #### 
import glob
import os
import sys
from datetime import datetime
print "\n** File renaming utility vers {0} **\n".format(vers)

# find the files - ask what to do with them
searchstring  = raw_input("File search string: ") or "file*"
files = glob.glob(searchstring)
files.sort()

print "\n"
if len(files) == 0:
    sys.exit("** ERROR no files found **")
for i in files:
    print i
print "\n{0} files to rename".format(len(files))

print "1) Keep original numbers \n2) Renumber sequenially" 
renumber = raw_input("")
if renumber not in ["1","2"]:
    sys.exit("**ERROR not an option**")

# keep the orginal numbers option

command = []
if renumber == "1":
        
    print "** example file name: **\n {0}".format(files[0])
    print "type the file with & replacing the numbers IE: file-001.txt = file-&.txt"
    filenametemplate = raw_input("file name template: ")
    front,back = filenametemplate.split("&")
    print "Enter template for new name. IE: 'file_****.txt' Number of *'s determines number of digits in the number"  
    newnamestring = raw_input("New name template: ") or "test_****.txt"
    if "." not in newnamestring:
        print "extension is missing... did you mean to do that?"
        ext = raw_input("extension (with .): ")
        newnamestring = "{0}{1}".format(newnamestring,ext)
    if "*" not in newnamestring:
        sys.exit("** ERROR no *'s in template **")
    digcount = newnamestring.count("*")
    print "\n"
    for i in files:
        newnameparts = newnamestring.split("*"*digcount)
        filenumber = i.replace(front,"")
        filenumber = filenumber.replace(back,"")
        newname = '{0}{1:0{2}d}{3}'.format(newnameparts[0],int(filenumber),digcount,newnameparts[1])
        print "{0} --> {1}".format(i,newname)
        command.append([i,newname])
    doit = raw_input("do it? (Y/N)?")

# sequential renumbering option

if renumber == "2":
    print "Enter template for new name. IE: 'file_****.txt' Number of *'s determines number of digits in the number"  
    newnamestring = raw_input("New name template:") or "test_****.txt"
    if "." not in newnamestring:
        print "extension is missing... did you mean to do that?"
        ext = raw_input("extension (with .): ")
        newnamestring = "{0}{1}".format(newnamestring,ext)
    if "*" not in newnamestring:
        sys.exit("** ERROR no *'s in template **")    
    digcount = newnamestring.count("*")
    newnameparts = newnamestring.split("*"*digcount)
    n = int(raw_input("Starting number: ")) or 1
    for i in files:
        newname = '{0}{1:0{2}d}{3}'.format(newnameparts[0],n,digcount,newnameparts[1])
        print "{0} --> {1}".format(i,newname)
        command.append([i,newname])
        n = n+1
    doit = raw_input("do it? (Y/N)?")

## open the logfile, move the files, and write the log
logout = open("RENAME.log", "a")
logout.write("\nrename utility vers {0} - {1}".format(vers,datetime.now()))

if doit == "y" or doit =="Y":
    for i in command:
        os.system("mv {0} {1}".format(i[0],i[1]))
        logout.write("\n{0} --> {1}".format(i[0],i[1]))
    print "{0} files renamed".format(len(command))
