#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the jumpingOnClouds function below.
def jumpingOnClouds(c):
    jumps = 0
    index = 0

    while index < len(c)-1:
        # if 2 cloud jumps
        if index+2 < len(c) and c[index+2] != 1:
            index += 1
        jumps += 1
        index += 1
    return jumps


if __name__ == '__main__':

    n = int(input())
    c = list(map(int, input().rstrip().split()))

    result = jumpingOnClouds(c)
    print(result)
    
