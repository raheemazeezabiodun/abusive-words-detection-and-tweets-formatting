import collections
import re
import sqlite3
import time
# step 2
# remove tweets indicated by rt
def remove_rt(string):
	return ''.join(word for word in string.split(' ') if not word.startswith('rt'))
a = remove_rt("hello rt:hdhd hdhj")

# step 3
# remove all symbols marked as @username
def remove_at_symbol(string):
	return ''.join(word for word in string.split(' ') if not word.startswith('@'))

# step 4
# remove all hashtags from tweets
def remove_hashtags(string):
	return ''.join(word for word in string.split(' ') if not word.startswith('#'))

# step 5 
# remove every repeated letter >= 3 with a single letter
def remove_duplicate(string):
	get_count = collections.Counter(string)
	seen = []
	for char in string:
		if char not in seen:
			if get_count[char] == 2:
				seen.append(char)
				#seen.append(char)	
			if get_count[char] >= 3:
				get_count[char] = 1
				seen.append(char)
			else :
				seen.append(char)
	return ''.join(seen)

#turn ass - butt to ass
def remove_hyphen_after_white_space(filename):
	with open(filename, 'rb') as infile, open('filtered.txt', 'wb') as outfile:
	    data = infile.read()
	    datan = re.sub(r'(\s)- \w+', r'\1', data)
	    #if not datan.startswith(" "):
	    outfile.write(datan)
	
remove_hyphen_after_white_space("badwords-dict.txt")

def search(s):
	empty = []
	import re
	formatted_sentence = []
	# remove any semicolon comma and leading whitespaces from our string
	tokenize_sentence = re.split('; |,| |\n',s)
	
	for x in tokenize_sentence:

		# call tweet formatting algorithm
		if len(x) > 0:
			# call remove_rt(s) function
			x1 = remove_rt(x)
		if len(x1) > 0:
			x2 = remove_at_symbol(x1)
		
		if len(x2) > 0:
			x3 = remove_hashtags(x2)
		
		if len(x3) > 0:
			x4 = remove_hashtags(x3)
		if len(x4) > 0:
			x5 = remove_duplicate(x4)
			formatted_sentence.append(x5)
		# check if formatted sentence contains abusive sentence
		# if x4 in open('filtered.txt', 'r').read():
			
		# 	if len(x4) != 1 and len(x4) > 1:	# if not a single letter and blank line
		# 		if x4 not in empty:
		# 			print x4
		# 			empty.append(x4)
		lines = open('filtered.txt' , "r" ).readlines()

		
		for line in lines:
		    if line.startswith(x5 + ' '):
		    	if x5 not in empty:
		    		empty.append(x4)
	print "Applying our algorithm for formatting tweet...."
	time.sleep(4)
	print "****--- formatted sentence is shown below --****\n"
	print formatted_sentence
		
	if len(empty) > 0:
		print "--------------------- %d Abusive words found ------------------" %(len(empty))
		print "----**** %s*****-----" %empty

		# it contains abusive words
		# insert into database
		try :
			db = sqlite3.connect('database.db')
			cursor = db.cursor()
			cursor.execute(''' INSERT INTO abusive(sentence, abusive_words, total_abusive_words) VALUES("%s","%s","%s")''' %(s, empty, len(empty)))
			db.commit()
			db.close()
			print "****** ----Abusive words detected!!!!!!!\n sentence sucessfuly stored into database with abusive words and its occurence ------********"
		except sqlite3.IntegrityError:
			print "The sentence exists already, try a new sentence"
	else :
		try :
			db = sqlite3.connect('database.db')
			cursor = db.cursor()
			cursor.execute(''' INSERT INTO non_abusive(sentence) VALUES("%s")''' %(s))
			db.commit()
			db.close()
			print "This sentence is free from abusive words!!!!!!!!!!!1\n sentence stored into database successfuly"
		except sqlite3.IntegrityError:
			print "This sentence already exists already, try a new sentence"
			
search("enter tweet sentence")
/usr/lib/jvm/java-7-openjdk-i386/jre/bin/java