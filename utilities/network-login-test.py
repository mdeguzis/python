#!/bin/python

# Description:
# Demonstrates logical operators and compound conditions
# Written in python2

security = 0
username = ""
password = ""

while not username:
    username = raw_input("Enter your username: ") 

while not password:
    password = raw_input("Enter your password: ")

if username == "mike" and password == "pizza":
    print "Hi Mike, have a nice day"
    security = 4

elif username == "admin" and password == "complexpassword":
    print "Welcome admin, system ready"
    security = 5

elif username == "guest" or password == "guest":
    print "Welcome guest"
    security = 1

else:
    print "Login failed! Access denied!"
    security = 0

