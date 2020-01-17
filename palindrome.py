#!/bin/python

#s1 = 'race car'
s1 = input("Enter string: ")

# Replace white space
# Case insensitive with casefold
# Make into a list ahead of time if you wish
s1 = list(s1.replace(" ","").casefold())

# reverse the string
# Case to list to avoid once-only iterator
rev_str = list(reversed(s1))

# you can consume an iterator only once
# If you do, rev_str will be blank later
# That's why rev_str is case to list above
print(list(s1))
print(list(rev_str))

# check if the string is equal to its reverse
if s1 == rev_str:
   print("The string is a palindrome.")
else:
   print("The string is not a palindrome.")

