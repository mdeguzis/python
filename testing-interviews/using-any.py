#!/usr/bin/python3
# Shows usage of any()
# any() returns:
#	True if at least one element of an iterable is true
#	False if all elements are false or if an iterable is empty

print('-' * 5 + 'numbers' + '-' * 5 + '\n')
# True
l = [1, 3, 4, 0]
print(any(l))

# False
l = [0, False]
print(any(l))

# True
l = [0, False, 5]
print(any(l))

# False
l = []
print(any(l))

print('\n' + '-' * 5 + 'strings' + '-' * 5)
s = "This is good"
print(any(s))

# 0 is False
# '0' is True
s = '000'
print(any(s))

s = ''
print(any(s))
