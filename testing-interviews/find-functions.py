import re

# Your code goes here
functs = sorted(dir(re))
find_members = []
for member in functs:
    if "find" in member:
        find_members.append(member)
print(find_members)

