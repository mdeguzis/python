#!/bin/python

# Firstly, a Nested Function is a function defined inside another function. It's
# very important to note that the nested functions can access the variables of
# the enclosing scope. However, at least in python, they are only readonly.
# However, one can use the "nonlocal" keyword explicitly with these variables in
# order to modify them.

def transmit_to_space(message):
    "This is the enclosing function"
    def data_transmitter():
        "The nested function"
        print(message)

    data_transmitter()

print(transmit_to_space("Test message"))

# This works well as the 'data_transmitter' function can access the 'message'. To
# demonstrate the use of the "nonlocal" keyword, consider this
# Without the nonlocal keyword, the output would be "3 9", however, with its usage,
# we get "3 3", that is the value of the "number" variable gets modified.

# The nonlocal keyword is used to work with variables inside nested functions,
# where the variable should not belong to the inner function.

def print_msg(number):
    def printer():
        # Here we are using the nonlocal keyword
        # If we deleted the next line,the file print in print_msg
        # would be 9, not 3
        nonlocal number
        number=3
        print(number)
    printer()
    print(number)

print_msg(9)

# ADVANTAGE : Closures can avoid use of global variables and provides some form
# of data hiding.(Eg. When there are few methods in a class, use closures
# instead).

# Exercise:
# Make a nested loop and a python closure to make functions to get multiple
# multiplication functions using closures. That is using closures, one could make
# functions to create multiply_with_5() or multiply_with_4() functions using
# closures.

def multiplier_of(n):
    def multiplier(number):
        return number*n
    return multiplier

multiplywith5 = multiplier_of(5)
print(multiplywith5(9))

