#!/bin/python

response = ""

while response != "that is the question.":
    # Python 2
    response = raw_input("Complete this phrase: To be or not to be, ")

    # Python 3
    #response = input("Complete this phrase: To be or not to be, ")

print "\nYou are correct!"
