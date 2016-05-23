#Author:  Joe Friedrich
#COhPy Challenge 2016-Apr solution
#
#Word is anything that is not a number or symbol.
#Single letter contractions have been removed.
#Single letters that are not 'offical' words have been removed.
#Examples:  The name 'Ra's al Ghul' would appear as 'Ra' and 'al' and 'Ghul'
#The name Sadu-Hem would appear as 'Sadu' and 'Hem'.
#
#Crap!  I missed the testing part :(
#Ah, well... here is what I have.
#
#Bonuses:  1,2,4,5

import requests
import re

#************************FUNCTIONS*****************************

def get_user_input():
	return input('Type the number of the Gutenberg publication you wish to see:  ')

def spam_gutenberg_website():
	return requests.get('http://www.gutenberg.org/cache/epub/' + book_number + '/pg' + book_number + '.txt')

def creating_a_dictionary(from_words_list):
	new_dictionary = {}
	for word in from_words_list:
    		if len(word) > 1:
        		if word in new_dictionary:
            			new_dictionary[word] += 1
        		else:
            			new_dictionary[word] = 1
    		elif word == 'A' or word == 'a' or word == 'I':
        		if word in new_dictionary:
        			new_dictionary[word] += 1
        		else:
            			new_dictionary[word] = 1
	return new_dictionary

def organizing_data(from_dictionary):
	organized_words = []
	for entry in from_dictionary.items():
		organized_words.append(entry)
	
	return sorted(organized_words, key = lambda entry: entry[1], reverse = 1)

#**************************START*******************************

print('Welcome to the Friedrich Gutenberg word-counter thingy.')
book_number = get_user_input()

print('\nGrabbing website data...')
website = spam_gutenberg_website()

find_book = re.split(r'\*{3}[\s\w]*\*{3}', website.text)
book = find_book[1]

find_words = re.compile(r'[a-zA-Z]+')
words = find_words.findall(book)

print('Creating dictionary...')
web_dictionary = creating_a_dictionary(words)

print('Organizing data...')
count_words = organizing_data(web_dictionary)

while(True):
	print('\nWhat would you like to see?')
	print('-Type a word to see how many times it appears.')
	print('-Type a number to see that number of top words.')
	print('-Type a super huge number to get all words.')
	user_choice = input('-Type q to quit:  ')
	print('')
	
	word_test = find_words.search(user_choice)
	
	if user_choice == 'q' :
		break
	elif word_test != None:
		if user_choice in web_dictionary:
			print(user_choice + ' => ' + str(web_dictionary[user_choice]))
		else:
			print('***The word does not appear in the text.***')
	else:
		user_choice = int(user_choice)
		if user_choice >= len(count_words):
			user_choice = len(count_words)
		for user_number in range(0, int(user_choice)):
			print(count_words[user_number])
