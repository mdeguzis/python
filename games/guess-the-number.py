#!/bin/python

# Description:
# Guess the number program written in python 2
# Demonstrates random numbers, loops, and math comparison

# import needed modules
import random

# set inital vars
the_number = random.randint(1,100)
tries = 0
range_check = 0

# Welcome screen
print \
'''
===================================
Random number guessing game
===================================

Guess the number between 1 and 100
The program AI will guess after you.

Can you beat the computer player?
''' 

# set intial player and computer input
player_guess = 0
computer_guess = 0
upper_bound = 100
lower_bound = 1
guess_type = "player"

# guessing loop

while player_guess != the_number or computer_guess != the_number:

    # compare guess against actual number

    if guess_type == "player":

        # player takes a guess
        # Make sure input positive is entered
        while player_guess <= 0: 

            player_guess = int(raw_input("Take a guess: "))
            tries += 1

        if player_guess > the_number:

            print "lower..."

        elif player_guess < the_number:

            print "higher..."

    elif guess_type == "computer":

        # computer takes a guess
        print "\nIt's the computer's turn to guess..."

        # Make the computer take a random initial guess
        computer_guess = random.randint(lower_bound,upper_bound)
    
        # set the upper and lower limits again based on guess

        if computer_guess > the_number:

            lower_bound = the_number
            upper_bound = computer_guess

        elif computer_guess < the_number:

            lower_bound = computer_guess
            upper_bound = the_number

    # Break out of the loop if the computer or player did guess the number
    if computer_guess == the_number:
        break

    elif player_guess == the_number:
        break

    # if the number is not guessed, switch players
    else:

        # switch player
        if guess_type == "player":

            # Reset player guess value to ensure proper input
            player_guess = 0
            guess_type = "computer"

        elif guess_type == "computer":

            print "The computer failed to guess correctly...\n"
            guess_type = "player"

    
# Fail or success condition
if computer_guess == the_number:
    print "\nYou lost! The number was: " + str(the_number)

elif player_guess == the_number:
    print "\nYou guessed the number! It was: " + str(the_number)
    print "You took: " + str(tries) + " tries to get it."


