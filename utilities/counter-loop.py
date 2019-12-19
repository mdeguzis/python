#!/bin/python

# Description: demonstrates a simple intentional infinite loop
# You want the loop to keep going and going, but at some point 
# if a break statment is hit, exit the loop.


count = 0 

while True:

    print count
    count += 1

    # end the loop if count great than 10
    if count > 10:
        # Break the loop
        break

    # skip 5
    if count == 5:
        # Keep going with the loop
        continue

print "The counter has reached: " +  str(count)
