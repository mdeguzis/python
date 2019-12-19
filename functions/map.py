#!/bin/python
# Description: test some map fundamentals
# What does it do?
#	Returns a list of the results after applying the given function  
#	to each item of a given iterable (list, tuple etc.) 
# Syntax:
#	map(function, iterable)
# See also:
#	https://www.w3schools.com/python/python_lambda.asp

def addition(n):
	""" return some math """
	return n + n

# We double all numbers using map() 
numbers = (1, 2, 3, 4) 
result = map(addition, numbers) 
print("---------------\nSimple example:\n---------------")
print("Input: ",numbers)
print("Output: ",list(result)) 

# lamba
print("\nWe can also use lambda expressions with map to achieve above result")
print("Input: ",numbers)
numbers = (1, 2, 3, 4) 
result = map(lambda x: x + x, numbers) 
print("Output: ",list(result)) 

print("\nAdd two lists using map and lambda")
numbers1 = [1, 2, 3] 
numbers2 = [4, 5, 6] 
print("Input1: ",numbers1)
print("Input2: ",numbers2)
  
result = map(lambda x, y: x + y, numbers1, numbers2) 
print("Output: ",list(result)) 

print("\nThe power of lambda is better shown when "
	+ "you use them as an anonymous function inside another function.")

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
print(mydoubler(11))

