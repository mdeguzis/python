#!/usr/bin/python3
a = ["Jake", "John", "Eric"]
b = ["John", "Jill"]
A = set(a)
B = set(b)

# Use of .difference requires set, it is not
# from use of a Python list
print(A.difference(B))

