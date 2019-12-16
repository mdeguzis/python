#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the countingValleys function below.
def countingValleys(n, s):
	sea_level = 0
	valley = 0

	for i in s:

		if i == 'U':
			sea_level += 1

		elif i=='D':
			sea_level += -1

		if sea_level == 0 and i == 'U':
		   valley += 1

	return valley


if __name__ == '__main__':

	#n = int(input())
	n = 12
	#s = input()
	s = "DDUUDDUDUUUD"

	result = countingValleys(n, s)
	print(result)

