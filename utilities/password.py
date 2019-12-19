#!/bin/python

# This program details some basic if functions

#
# Password program
#

print "\nWelcome to PythonPass\n"

password = raw_input("Enter your password (Hint: Tom's favorite coffee): ")

# If the password is secret, accept it, if it is false, do not
if (password == "costco" or "kirkland"):
    print "Access granted!"
else:
    print "Access denied!"

raw_input("Press any key to exit\n")
