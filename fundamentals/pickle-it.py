#!/usr/bin/python2

# Demonstrates pickling and shelving data
# pickles, stores, and retrieves three lists of strings in a binary file

import pickle, shelve

# First, create the three lists that I plan to pickle and write to a file.
print "Pickling lists..."
variety = ["sweet", "hot", "dill"]
shape = ["whole", "spear", "chip"] 
brand = ["Claussen", "Heinz", "Vlassic"]

# open the new file to store the pickled lists
# mode 'wb' - Write to a binary file
f = open("pickles1.dat", "wb")

# pickle and store the three lists variety, shape, and brand in the 
# file pickles1.dat using the pickle.dump() function function requires 
# two arguments: the data to pickle and the file in which to store it.

pickle.dump(variety, f)
pickle.dump(shape, f)
pickle.dump(brand, f)
f.close()

# this code pickles the list referred to by variety and writes the 
# whole thing as one object to the file pickles1.dat. 
# Next, the program pickles the list referred to by shape and writes the
# whole thing as one object to the file. 
# Then, the program pickles the list referred to by brand and writes 
# the whole thing as one object to the file. Finally, the program closes the file.

# read the data
print "\nUnpickling lists."
f = open("pickles1.dat", "rb")
variety = pickle.load(f)
shape = pickle.load(f)
brand = pickle.load(f)

# output the lists
print(variety)
print(shape)
print(brand)
f.close()

# Using shelf to store pickled data
# create a 'shelf' that acts like a dictionary, providing random access
# to the lists

print "\nShelving lists"
s = shelve.open("pickles2.dat")

# add three lists to the shelf:
s["variety"] = ["sweet", "hot", "dill"]
s["shape"] = ["whole", "spear", "chip"]
s["brand"] = ["Claussen", "Heinz", "Vlassic"]

# Invoke the shelf's sync() method
# make sure data is written
s.sync() 

print "\nRetrieving lists from a shelved file:"
print "brand -", s["brand"]
print "shape -", s["shape"]
print "variety -", s["variety"]

s.close()

raw_input("\nPress any key to exit")
