#!/bin/python
#Both players are given the same string,
#Both players have to make substrings using the letters of the string

#Stuart has to make words starting with consonants.
#Kevin has to make words starting with vowels.
#The game ends when both players have made all possible substrings.

#Scoring
#A player gets +1 point for each occurrence of the substring in the string

def minion_game(string):
    vowels = 'AEIOU'
    kevsc = 0
    stusc = 0

    # Test each index of user's string
    # Use implicit count of occurrence
    for i in range(len(s)):
        if s[i] in vowels:
            kevsc += (len(s)-i)
        else:
            stusc += (len(s)-i)

    if kevsc > stusc:
        print("Kevin", kevsc)
    elif kevsc < stusc:
        print("Stuart", stusc)
    else:
        print("Draw")

if __name__ == '__main__':
    s = input()
    minion_game(s)
