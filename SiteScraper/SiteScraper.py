# Imports required libraries
from lxml import html
import requests
import re

# Submission array indeces:
# sub[0]: name
# sub[1]: id#
# sub[2]: want to draw,
# sub[3]: want to receive
# sub[4]: backup santa or not
# sub[5]: post link
# sub[6]: tier

# ---- NEED TO UPDATE EVERY YEAR -----

# Set the number of pages to look through
numOfPages = 12
# Initial posts to skip
numInitialPosts = 5 
# URL to search for submission posts
url = 'https://www1.flightrising.com/forums/cc/2767227'

# -------------------------------------

# Key words to determine what the user wants
yesWords = ['yes', 'yup', 'sure', 'yep', 'okay', 'ok', 'of course', 'definitely']
noWords = ['no', 'nah', 'nope', 'not']

dragonCat = r'FR Dragons'
humanCat = r'Human/Gijinka'
anthroCat = r'Anthro'
feralCat = r'Non-FR Ferals'
noCat = r'No Preference'

# Error log to track any oddities or problems
error_log = []

# Retrieves HTML from a given URL and stores it in an organized tree
page = requests.get(url)
tree = html.fromstring(page.content)

# The path to find the max number of pages in the thread
# Looks for the div where the navigable page numbers are held and finds the last one
pageNumPath = '//div[@class=\'common-pagination-numbers\']/a[last()]/text()'
# Path for the posts
postPath = '//div[@class=\'post \' or @class=\'post  no-signature\']'
# Get the string value of the post's ID to get its direct link
IDPath = 'string(./@id)'
# Path to the content of the post, loking only at plain text
contentPath = 'string(.//div[@class=\'post-text-content\'])'

# Find the element according to the path
endPageNums = tree.xpath(pageNumPath)

# This is where all submissions are stored for stats
submissions_stats = []

# Takes a list of submissions and returns a string directory from it, encoded
def genDirectoryText(submissions):
	text = ""
	# Loop through all submissions in the list and generate the directory
	for sub in submissions:
		text += ("[url=" + sub[5] + "]" + sub[0] + "[/url]" + " " + u'\u2022' + " ")
	# Return the resulting string minus the extra bullet at the end
	return text[:-3].encode('utf-8')

# Sorts and returns the list
def alphabeticSort(list):
	return sorted(list, key=lambda s: s[0].lower())

# Takes submissions and filters them by the index corresponding to the specified value
def filterBy(submissions, index, restriction):
	newSubmissions = []
	# Check all submissions and only include those that match
	# either the highest preference of the receive, or the tier
	for sub in submissions:
		if sub[index][0] == restriction:
			newSubmissions.append(sub)
	return newSubmissions

# Takes list of submissions and creates the pinglist for it
def genPinglist(submissions):
	text = ""
	for sub in submissions:
		text += "@" + sub[0] + " "
	return text

# Get the string from the specified field in the given post's string
def getValue(field, string, errors):
	# Create regex to find the field, and create match object for that entire line
	match = re.search(field + '.*\n', string, flags=re.IGNORECASE)
	# If match exists, return the string right after the field's text, stripped of whitespace
	if match:
		return string[(match.start(0)+len(field)):match.end(0)].strip()
	else:
		#print('Error occured trying to get the value for ' + field + '!\n')
		errors.append("Could not get " + field + "!\n")

# Clean function for matching key words
def matchFor(field, strList, string):
	return re.search(field + '(.*(' +  '|'.join(strList)+').*)*\n', string, flags=re.IGNORECASE)

def getRankings(field, string):
	return re.search('(' + field + '\n*)\n*((.*\n)+?)\n*?(\s?What|\s?Please)', string, flags=re.IGNORECASE) 

def findPref(category, stringToSearch):
	return re.search(category, stringToSearch, flags=re.IGNORECASE)

# Takes the question to search for amongst the given block of text
# Returns a string of characters ordered from greatest preference to least
def determinePref(field, string, errors):
	# An array with the rank ordered
	prefRank = []

	rankings = getRankings(field, string)

	if not rankings:
		errors.append("Failed to find rankings")
		return '?'

	# Retrieve all lines that aren't blank
	pattern = re.compile(r'((.+)\n)+?')

	# Iterate through each non blank line to determine preference for each ranking
	for match in re.finditer(pattern, rankings.group(2)):
		if match.group(0) == '':
			pass

		preference = []

		likesDragon = findPref(dragonCat, match.group(2))
		likesHuman = findPref(humanCat, match.group(2))
		likesFeral = findPref(feralCat, match.group(2))
		likesAnthro = findPref(anthroCat, match.group(2))
		likesNone = findPref(noCat, match.group(2))

		if likesDragon:
			preference.append('d')
		if likesHuman:
			preference.append('h')
		if likesFeral:
			preference.append('f')
		if likesAnthro:
			preference.append('a')
		if likesNone:
			preference.append('n')

		if len(preference) == 0:
			prefRank.append('?')
			errors.append("Couldn't determine preference for %s?" % (field))
		elif len(preference) > 1:
			prefRank.append('?')
			errors.append("Multiple preferences listed for %s?" % (field))
		else:
			prefRank.append(preference[0])

	if len(prefRank) > 4:
		errors.append("Ranked more than 4 items for %s?\nErr: %d\n" % (field, len(prefRank)))
	elif len(prefRank) < 4:
		errors.append("Ranked fewer than 4 items for %s?\nErr: %d\n" % (field, len(prefRank)))

	return ''.join(prefRank)

# Determines if they want to be backup santa or not
def yesOrNo(string, errors):
	yesMatch = matchFor('Would you like to sign up as a Backup Santa\\?', yesWords, string)
	noMatch = matchFor('Would you like to sign up as a Backup Santa\\?', noWords, string)

	if yesMatch:
		if noMatch:
			#print('Included yes and no?')
			errors.append('**Yes and no for backup santa.**\n')
			return "?"
		return "Yes"
	elif noMatch:
		return "No"
	else:
		#print('Didn\'t specify backup santa?')
		errors.append('**Unknown input for backup santa.**\n')
		return "?"

if len(endPageNums) != 0:
	numOfPages = endPageNums[0]

# Open files for writing the matching input
fileTierA = open('signups_tierA.tsv', 'w+')
fileTierB = open('signups_tierB.tsv', 'w+')

# Check through every page in the thread, including the last one, since it is not 0 indexed
for page in range(1, int(numOfPages)+1):
	print("\n\t>>> Now scanning page " + str(page) + "/" + str(numOfPages) + "<<<\n")
	# Accessing the new page by adding its number at the end of the thread's url
	pageHTML = requests.get(url + '/' + str(page))
	tree = html.fromstring(pageHTML.content)

	# Get all posts
	posts = tree.xpath(postPath)

	# Skip non-user posts
	if page == 1:
		posts = posts[numInitialPosts:]

	# This is where each submission is stored for matching
	signupsTierA = []
	signupsTierB = []

	# Loop through all submission posts
	for post in posts:
		submission = []
		# For tracking any errors that might arise
		errors = []

		postContent = post.xpath(contentPath)
		
		errors.append("----\n")

		# Find the username
		submission.append(getValue('Username:', postContent, errors))

		# Find the id
		submission.append(getValue('ID:', postContent, errors))

		errors.append(submission[0] + ' - ' + submission[1] + '\n')

		# Find the draw preference
		submission.append(determinePref('Please rank your -drawing- preferences:', postContent, errors))

		# Find the receive preference
		submission.append(determinePref('Please rank your -receiving- preferences:', postContent, errors))

		# Find backup santa or no
		submission.append(yesOrNo(postContent, errors))

		# Add the link to the post
		submission.append(url + '/' + str(page) + '#' + post.xpath(IDPath))

		# Find the tier
		submission.append(getValue('What tier would you like to be in?', postContent, errors))

		# Add the submission to the stats array
		submissions_stats.append(submission)

		# Combine submission list, minus the tier, into a tab separated string and add it to the appropriate tier list
		info = '\t'.join(submission[:-1])

		if submission[6] == 'A':
			signupsTierA.append(info)
		elif submission[6] == 'B':
			signupsTierB.append(info)
		else:
			errors.append("Could not determine Tier (default to B)")
			signupsTierB.append(info)

		errors.append(submission[5] + '\n')

		# Write to error log if any errors occur.
		if len(errors) > 3:
			error_log.append('\n'.join(errors))

	# Combine all submissions into a string
	submissionsTierA = '\n'.join(signupsTierA)
	submissionsTierB = '\n'.join(signupsTierB)
	
	# Store submissions into the file
	fileTierA.write(submissionsTierA.encode('utf-8') + '\n')
	fileTierB.write(submissionsTierB.encode('utf-8') + '\n')

fileTierA.close()
fileTierB.close()
print("Wrote signups successfully")


print("Writing directory to file")
# Open file for writing to the directory
f = open('directory.txt', 'w+')

# By Post Order
f.write("[b]By Post Order:[/b]\n" + genDirectoryText(submissions_stats) + "\n\n")

# Alphabetically
f.write("[b]Alphabetical:[/b]\n" + genDirectoryText(alphabeticSort(submissions_stats)) + "\n\n")

# Note, could technically reduce run time by breaking apart the array during filtering
# TODO do something like this or just count to make sure the total matches the number in each category!

f.write("[b]Want Dragon Art:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 3, 'd'))) + "\n\n")

f.write("[b]Want Human Art:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 3, 'h'))) + "\n\n")

f.write("[b]Want Anthro Art:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 3, 'a'))) + "\n\n")

f.write("[b]Want Feral Art:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 3, 'f'))) + "\n\n")

f.write("[b]No Preference:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 3, 'n'))) + "\n\n")

f.write("[b]Tier A:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 6, 'A'))) + "\n\n")

f.write("[b]Tier B:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, 6, 'B'))) + "\n\n")

# Stats
f.write('\n\nTotal Participants: [b]' + str(len(submissions_stats)) + '[/b]')

f.close()
print("Wrote directory successfully")

print("Writing pinglist to file")
# Generating pinglist
f = open ('pinglist.txt', 'w')
f.write(genPinglist(alphabeticSort(submissions_stats)).encode('utf-8') + "\n")
f.close()
print("wrote pinglist successfully")

print("Writing error log to file")
# Generating error/exception log
error_log = ''.join(error_log) 
f = open('error_log.txt', 'w')
f.write(error_log.encode('utf-8'))
f.close()
print("Wrote error log successfully")

print("DONE")