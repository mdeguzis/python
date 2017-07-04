#!/usr/bin/python2

user = 'testuser'
filename = '/tmp/passwd'

"""Remove lines from start ot end"""
tempfile = open(filename)
templist = []
for linenum, line in enumerate(tempfile):
	if user in line:
		# do next line, line without append
		continue
	templist.append(line)
tempfile.close()
tempfile = open(filename, 'w')
tempfile.writelines(templist)
tempfile.close()
