#!/usr/bin/env python2

# Description: demonstrates len() and the 'in' operator
# Written in python 2

message = raw_input("\nEnter a message: ")

# count the length of the message
print "The length of the message is:", len(message)

print "\nThe most common letter in the English language, 'e',"

# The 'in' operator will search for "e" inside the var contents
if "e" in message:
    print("is in your message.\n")
else:
    print("is not in your message.\n")
