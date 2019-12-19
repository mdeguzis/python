#!/bin/python3

import os
import sys

#
# Complete the simpleArraySum function below.
#
def simpleArraySum(ar):
    #
    # Write your code here.
    #
	x = 0
	for i in ar:
		x += i
		print("x is:",x)
	return x

if __name__ == '__main__':

	ar_count = int(input())
	ar = list(map(int, input().rstrip().split()))

	result = simpleArraySum(ar)
	print(result)


