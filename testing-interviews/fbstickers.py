#!/bin/python

# Facebook logo stickers cost $2 each from the company store. I have an idea.
# I want to cut up the stickers, and use the letters to make other words/phrases.
# A Facebook logo sticker contains only the word 'facebook', in all lower-case letters.
#
# Write a function that, given a string consisting of a word or words made up
# of letters from the word 'facebook', outputs an integer with the number of
# stickers I will need to buy.
#
# get_num_stickers('coffee kebab') -> 3
# get_num_stickers('book') -> 1
# get_num_stickers('ffacebook') -> 2
#
# You can assume the input you are passed is valid, that is, does not contain
# any non-'facebook' letters, and the only potential non-letter characters
# in the string are spaces.

def get_num_stickers(input_string):
	
	# 1 sticker will always be used
	stickers_used = 1
	sticker_string = list('facebook')
	invalid_chars = [' ']
	letters = list(input_string)

	while letters:
		for l in letters:
			# Trim invalid chars
			if str(l) in invalid_chars:
				letters.remove(l)

			print("DEBUG: looking for letter: '" + str(l) + 
				"' against sticker bank: " + str(sticker_string))
			try:
				if len(sticker_string) == 0:
					# Sticker bank empty, reset it
					sticker_string = list('facebook')	
					stickers_used += 1
					
				# If this letter matches a sticker letter, remove
				if str(l) in sticker_string:
					sticker_string.remove(l)
					letters.remove(l)
					continue

				elif str(l) not in sticker_string:
					if len(sticker_string) >= 2 and len(letters) >= 2:
						# Looks like the letter is not in the sticker
						# since we have at least 2 letters, try again
						continue
					else:
						# We must only have one leter and it's not found
						# reset the sticker
						sticker_string = list('facebook')	
						stickers_used += 1
						continue
			
			except:
				raise

	return stickers_used

input_string = raw_input("What is the string" +
	" you want to make out of facebook stickers?: ")

stickers_used = get_num_stickers(input_string)
print("Stickers used: " + str(stickers_used))
