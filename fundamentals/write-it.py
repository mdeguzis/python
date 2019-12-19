#!/usr/bin/python

# Write It
# Demonstrates writing to a text file

# opening the file in write mode here wipes out it's contents
print "\nCreating a text file with the write() method."
text_file = open("write_it.txt", "w")

text_file.write("Line 1\n")
text_file.write("This is line 2\n")
text_file.write("That makes this line 3\n")
text_file.close()

print "Reading the newly created file."
text_file = open("write_it.txt", "r")
print(text_file.read())
text_file.close()

print "\nCreating a text file with the writelines() method."
text_file = open("write_it.txt", "w")

# write strings to the file
# writelines() is much like it's counterpart, readlines()

lines = ["Line 1\n",
	"This is line 2\n",
	"That makes this line 3\n"]

# write the tnere list of strings to the file with writelines()
text_file.writelines(lines)

text_file.close()

# print the contents to show the new file is exactly the same as the old
print "\nReading the newly created file."
text_file = open("write_it.txt", "r")
print text_file.read()
text_file.close()

# Now use 'with open' to demonstrate the difference
# For this demonstration, we must use a different filename, as the 
# previous file is closed foribly above
# This is why 'with open' shines, it is much more capable and manageable

print "\nCreating a text file with the write() method using 'with open'."
with open("write_it.txt", 'w') as text_file:
	text_file.write("Line 1\n")
	text_file.write("This is line 2\n")
	text_file.write("That makes this line 3\n")

# read the new file
with open("write_it.txt", 'r') as text_file:
	print text_file.read()

raw_input("Press enter to exit.")
