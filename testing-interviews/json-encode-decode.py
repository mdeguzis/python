#!/usr/bin/python3
import json

# Serialization is a mechanism of converting the state of an object into a
# byte stream. Deserialization is the reverse process where the byte stream
# is used to recreate the actual Java object in memory. ... So, the object
# serialized on one platform can be deserialized on a different platform.

# fix this function, so it adds the given name
# and salary pair to salaries_json, and return it
def add_employee(salaries_json, name, salary):
    # encode the data back into to JSON structure
    salaries = json.loads(salaries_json)
    # Add item to dictionary
    salaries[name] = salary

    # Return the deserialized JSON object (string)
    return json.dumps(salaries)

# test code
salaries = '{"Alfred" : 300, "Jane" : 400 }'
new_salaries = add_employee(salaries, "Me", 800)
decoded_salaries = json.loads(new_salaries)
print(decoded_salaries["Alfred"])
print(decoded_salaries["Jane"])
print(decoded_salaries["Me"])
