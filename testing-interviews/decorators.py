#!/bin/python
# Decorators allow you to make simple modifications to callable objects like
# functions, methods, or classes. We shall deal with functions for this
# tutorial. The syntax

def repeater(old_function):
    # See learnpython.org/page/Multiple%20Function%20Arguments for how *args and **kwds works
    def new_function(*args, **kwds): 
	# we run the old function
        old_function(*args, **kwds)
	# we do it twice
        old_function(*args, **kwds)

    # we have to return the new_function, or it wouldn't reassign it to the value
    return new_function 

# Apply the decorator with the @ shortcut
@repeater
def multiply(num1, num2):
    print(num1 * num2)
multiply(2,3)

# Make a decorator factory which returns a decorator that decorates functions
# with one argument. The factory should take one argument, a type, and then
# returns a decorator that makes function should check if the input is the
# correct type. If it is wrong, it should print("Bad Type") (In reality, it
# should raise an error, but error raising isn't in this tutorial). Look at
# the tutorial code and expected output to see what it is if you are confused
# (I know I would be.) Using isinstance(object, type_of_object) or
# type(object) might help.

def type_check(correct_type):
    def check(old_function):
        def new_function(arg):
            if (isinstance(arg, correct_type)):
                return old_function(arg)
            else:
                print("Bad Type")
        return new_function
    return check

@type_check(int)
def times2(num):
    return num*2

print(times2(2))
times2('Not A Number')

@type_check(str)
def first_letter(word):
    return word[0]

print(first_letter('Hello World'))
first_letter(['Not', 'A', 'String'])
