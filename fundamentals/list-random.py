#!/usr/bin/python

# Print a random list of words

old_list=["hello","bye","good night","welcome"]
new_list=[]

import random

while len(new_list) != len(old_list):

	word=random.choice(old_list)

	if word not in new_list:

		new_list.append(word)

print new_list
