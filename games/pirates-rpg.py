#!/bin/python

# Description:
# This program simulates a simple RPG balle with a while lop
# The purpose of this program is to illustrate if statments
# and while loops
# It is written on python 2
#
# Author: Michael T. DeGuzis
# Date:   20161231 18:54 UTC -4

import random
import sys

print \
'''===========================================
Pirates of the Carribean RPG
===========================================

        \      \\
         \      \\
        ||\    ||\ 
 __     || |   || |
|  |____||/____||/__________
\                       /
 \_____________________/

Your ship has been boarded by 4 pirates!
Can Captain Jack Sparrow defeat them all?

The player has 20 health
Each pirate has 8 health
 
unguard!
===========================================
'''

start_game = raw_input("Start the battle? [yes|no]: ")

# Start game or exit out
if start_game != "yes":
    sys.exit("You coward!\n")

# Start main function with expected vars to receive
def battle_function(player_dmg_multi, enemy_dmg_multi, enemy_name, enemy_type, enemy_health):

    # Set global values to return back out of function
    global player_health
    global enemy_num
    global enemies_remaining

    print \
'''
=====================
Battle Mode!
=====================
'''

    if enemy_type == "boss":
        print "Watch out! A boss approaches! It's " + enemy_name + "!!!"

    elif enemy_type == "regular":
        
        print "Watch out, a " + enemy_name + " approaches!"
        raw_input("Press enter")

    while enemy_health > 0:

        # Set random chance for attack
        attack_chance = random.randint(1,2)

        if attack_chance == 1:

            # enemy attack
            print "\n= The enemy attacks! ="
            damage = random.randint(1,2)
            total_damage = damage * enemy_dmg_multi
            player_health = player_health - total_damage

            print \
'''    _____
   /     \       
  | SLASH |
   \_____/
'''

            print "You take: " +  str(total_damage) + " damage"

            # Only print health if player health is not <= 0
            if player_health > 0:
                print "Player health remaining: " + str(player_health)
                raw_input("\nPress enter")

            elif player_health <= 0:
                sys.exit("You are dead!")

        elif attack_chance == 2:

            # Player attack
            print "\n= You attack the enemy ="
            damage = random.randint(1,4)
            total_damage = damage * player_dmg_multi
            enemy_health = enemy_health - total_damage

            print \
'''    __________
   /          \       
  | TAKE THAT! |
   \__________/
'''

            print "You inflict: " + str(total_damage) + " damage on the enemy"

            # Only print health if pirate health is not <= 0
            if enemy_health > 0:
                print "Enemy health remaining: " + str(enemy_health)
                raw_input("\nPress enter")
 
            else:
                # Enemy health is 0, enemy defeated
                print "\n== Enemy " + str(enemy_num) + " is defeated! =="
                enemy_num += 1
                enemies_remaining -= 1 

                print "== Enemies remaining: " + str(enemies_remaining) + " =="
                print "== Player health remaining: " +str(player_health) + " =="
                raw_input("\nPress enter to continue")
#
# Main
#

# Start main battle

# Initialize vars
player_dmg_multi = 1
enemy_dmg_multi = 1
player_health = 25
enemy_name = "pirate"
enemy_num = 1
enemy_type = "regular"
enemy_health = 8
enemies_remaining = 4

# Initial battles until no enemies remain
while enemies_remaining > 0:

    # Initiate battle with our default enemy health
    battle_function(player_dmg_multi, enemy_dmg_multi, enemy_name, enemy_type, enemy_health)

    # DEBUG ONLY - check values after fucntion is ran
    #print "New Health: ", player_health 
    #print "Check enemy name ", enemy_name
    #print "New enemy num: ", enemy_num
    #print "New enemmy type: ", enemy_type
    #print "Ensure enemy health is reset: ", enemy_health
    #print "New enemies remaing: ", enemies_remaining

# Give player new weapon
print "\nYou gain a new sword! Gain x 2 damage multiplyer!"
player_dmg_multi = 2

# Random boss battle
boss_battle_init = random.randint(1,2)

if boss_battle_init == 1:

    print \
'''
===============================
RANDOM BOSS BATTLE !
==============================='''    
    enemy_type = "boss"
    enemy_name = "Black beard"
    enemy_num = 1
    enemies_remaining = 1
    enemy_dmg_muti = 2
    boss_health = 15
    enemy_health = boss_health
    battle_function(player_dmg_multi, enemy_dmg_multi, enemy_name, enemy_type, enemy_health)    

print \
'''

============================================
.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
You are victorious (cue: FF7 battle music)
.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
============================================

'''
