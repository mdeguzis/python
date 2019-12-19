# Sets are lists with no duplicate entries. Let's say you want to collect a
# list of words used in a paragraph:
print("\nGive me 'my name is Eric and Eric is my name' (no duplicates)")
print(set("my name is Eric and Eric is my name".split()))

# Sets are a powerful tool in Python since they have the ability to
# calculate differences and intersections between other sets. For example,
# say you have a list of participants in events A and B:
a = set(["Jake", "John", "Eric"])
print(a)
b = set(["John", "Jill"])
print(b)

# To find out which members attended both events, you may use the
# "intersection" method:
a = set(["Jake", "John", "Eric"])
b = set(["John", "Jill"])

print(a.intersection(b))
print(b.intersection(a))

