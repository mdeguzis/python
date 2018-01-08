# Description: Check elements in a JSON file that contains dictionary items

import json

filename = raw_input("Log file to parse: ")

with open(filename,'r') as j:
	json_dict = json.load(j)
	for key,value in json_dict.iteritems():
		print "Key: " + str(key)
		print "Value: " + str(value)

