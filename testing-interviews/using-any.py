#!/usr/bin/python3
# Shows usage of any()
# any() returns:
#	True if at least one element of an iterable is true
#	False if all elements are false or if an iterable is empty

print('-' * 5 + 'numbers' + '-' * 5)
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

print('\n' + '-' * 5 + 'conditional s' + '-' * 5)

# At least one is true, returs true
x = [-1,0,1]
y = [1,2,3]
if any(t < 0 for t in x):
    # do something`
	print("At least one is true")

if any(t2 < 0 for t2 in y):
	# None are true, this never happens
	print("At least one is true")
else:
	print("All of these are false!")




