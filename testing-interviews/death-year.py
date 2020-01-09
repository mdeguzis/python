#!/bin/python
# Given a list of birth dates and death dates,
# find the year with the highest population

import json

# Flat data should be fine, use list of tuples
data = [
    ('Tom',1860,1930),
    ('Edith',1960,1990),
    ('Paul',1945,1999),
    ('karen',1730,1811),
    ('Carl',1930,1990)
]

# Get our min and max out of the ranges
min_bdate = min(d[1] for d in data)
max_ddate = max(d[2] for d in data)

# from the first birth, to latest death,
# How many of these people where alive in the year
year_pop = {}
for d in range(min_bdate,max_ddate):
    pop_num = 0
    year_pop[d] = {}
    year_pop[d]['names'] = []
    year_pop[d]['total_pop'] = pop_num
    year_pop[d]['most_pop'] = False
    for p in data:       
        name = p[0]
        bdate = p[1]
        ddate = p[2]
        if bdate <= d and d < ddate and name not in year_pop[d]['names']:
            pop_num += 1
            year_pop[d]['total_pop'] = pop_num
            year_pop[d]['names'].append(name)

# test date
print(json.dumps(year_pop, indent =4))

