# initialize a list
initList = ['camel', 'case', 'stop']

# print each words using loop
print('Printing using default print function')
for item in initList:
    print(item)  # default print function. newline is appended after each item.

print()  # another newline

# print each words using modified print function
# The 'end' parameter modifies the seperate
print('Printing using modified print function')
for item in initList:
    print(item, end='')

print('\n')
