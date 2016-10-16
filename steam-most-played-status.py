#!/bin/python

#########################################################
# CREDIT: Code Artisan 
# Profile: (https://www.gamingonlinux.com/profiles/4240)
#########################################################

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import sys

def eprint(*args, **kwargs):
    print("[STDERR]", *args, file=sys.stderr, **kwargs)

# Scrape steam's stats
eprint("Scraping steam's stats page...")
html = urlopen("http://store.steampowered.com/stats/")
bs = BeautifulSoup(html.read(), "html.parser")
topGamesTr = bs.findAll("tr", class_="player_count_row")

# Table columns
topGames = [["Current Players"],
            ["Peak Today"],
            ["Game Name"],
            ["Status"]]

total            = len(topGamesTr)
totalSupported   = 0
totalUnsupported = 0
totalUnknow      = 0

# Fetch games information to fill table columns
for i, gameTr in enumerate(topGamesTr):
    eprint("Processing game", i, "on", total, "...")
    # Current Players
    topGames[0].append(gameTr.contents[1].contents[1].contents[0])
    # Peak Today
    topGames[1].append(gameTr.contents[3].contents[1].contents[0])
    # Game Name
    topGames[2].append(gameTr.contents[7].contents[1].get_text())
    # Game store address
    url = gameTr.contents[7].contents[1].get("href")    
    # Has the game a store page ?
    if url.startswith("http://store.steampowered.com/app/"):        
        # Retrieves game's information from the steam store (JSON)
        url = url.replace("app/", "api/appdetails?appids=")[:-1]
        js = json.loads(urlopen(url).read().decode('utf-8'))      
        for d in js:           
            # Is linux supported ?
            if js[d]["data"]["platforms"]["linux"]:
                totalSupported += 1
                status = "SUPPORTED"
            else:
                totalUnsupported += 1
                status = "UNSUPPORTED"
    else:
        totalUnknow += 1
        status = "UNKNOW"                      
    topGames[3].append(status)

# Format of table is column major
#  [(header1|row1|row2),
#   (header2|row1|row2),
#   ...]       
def printTable (table):
    columnAmount = len(table)
    columnsWidth = [0] * columnAmount
    rowAmount    = len(table[0])    
    # grab columns width and print the headers
    for i in range(columnAmount):
        columnsWidth[i] = max([len(x) for x in table[i]])
        print("{0:>{1}}".format(table[i][0],columnsWidth[i]),end="")
        if i+1<columnAmount:
            print(" | ", end="")
    print("") 
    # print separation row
    for i in range(columnAmount):
        print("-" * columnsWidth[i], end="")
        if i+1<columnAmount:
            print(" | ", end="")
    print("")   
    # print elements rows
    for i in range(1, rowAmount):
        for j in range(columnAmount):
            print("{0:>{1}}".format(table[j][i],columnsWidth[j]),end="")
            if j + 1 < columnAmount:
                print(" | ", end="")
        print("")

eprint("")
printTable(topGames)
print("")
print("{:>12}: {:>5}".format("TOTAL", total))
print("{:>12}: {:>5}".format("SUPPORTED", totalSupported))
print("{:>12}: {:>5}".format("UNSUPPORTED", totalUnsupported))
print("{:>12}: {:>5}".format("UNKNOW", totalUnknow))
