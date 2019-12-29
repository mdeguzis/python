#!/usr/bin/python3

# Partial functions You can create partial functions in python by using the
# partial function from the functools library.
# 
# Partial functions allow one to derive a function with x parameters to a
# function with fewer parameters and fixed values set for the more limited
# function.

# create a new function that multiplies by 2:
# An important note: the default values will start replacing variables from
# the left. The 2 will replace x. y will equal 4 when dbl(4) is called. It
# does not make a difference in this example, but it does in the example
# below.

from functools import partial

def multiply(x,y):
    return x * y


dbl = partial(multiply,2)
print(dbl(4))

# Partial functions allow us to fix a certain number of arguments of a
# function and generate a new function.

# A normal function 
def f(a, b, c, x): 
    return 1000*a + 100*b + 10*c + x 
  
# A partial function that calls f with 
# a as 3, b as 1 and c as 4. 
# Replacement is done left to right
g = partial(f, 3, 1, 4) 
  
# Calling g() 
# This simply then defines 5 into the next
# availble positional argument, x, as
# the first there are defined and fixed now
# with the partial function
print(g(5)) 

'''
Exercise:
Edit the function provided by calling partial() and replacing the first
three variables in func(). Then print with the new partial function using
only one input variable so that the output equals 60.
'''

#Following is the exercise, function provided:
from functools import partial
def func(u,v,w,x):
    return u*4 + v*3 + w*2 + x
    
#Enter your code here to create and print with your partial function
pfunct = partial(func,2,4,6)
print("pre-return math: ")
print(2*4 + 4*3 + 6*2)
print(pfunct(28))


