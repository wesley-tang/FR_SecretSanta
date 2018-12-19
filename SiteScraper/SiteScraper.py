# Imports required libraries
from lxml import html
import requests
import re

# Note: sub[0]: name, sub[1]: id#, sub[2]: want to draw,
# sub[3]: want to receive, sub[4]: backup santa or not, sub[5]: post link

# Key words to determine what the user wants
yesWords = ['yes', 'yup', 'sure', 'yep', 'okay', 'ok', 'of course', 'definitely']
noWords = ['no', 'nah', 'nope', 'not']

dragonWords = ['dragon', 'feral']
humanWords = ['human', 'anthro', 'humanoid', 'gijinka', 'gij']
noPrefWords = ['no preference', 'no pref']

prefWords = ['preferred', 'prefer']
onlyWords = ['only']

# Error log to track any oddities or problems
error_log = []

# URL to search for submission posts
url = 'http://www1.flightrising.com/forums/cc/2554259'

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

# Takes submissions and filters them by what the submitter wants drawn
def filterBy(submissions, restric1, restric2):
	newSubmissions = []
	# Check all submissions and only include those that match the criteria.
	for sub in submissions:
		if sub[3].lower() == restric1 or sub[3].lower() == restric2:
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

# Figures out what preference the person wants, dragon or human
def determinePref(field, string, errors):
	# 0 is no pref, 1 is drag, 2 is human
	pref = 0
	only = True

	# Check if keywords are found for each category
	dragMatch = matchFor(field, dragonWords, string)
	humMatch = matchFor(field, humanWords, string)
	noPrefMatch = matchFor(field, noPrefWords, string)

	# Determine preference based on if the matches are found
	if dragMatch:
		if humMatch:
			#print('Included drag and human??\n\n')
			errors.append("**Preferences match multiple categories**.\n")
		else:
			pref = 1
	elif humMatch:
		pref = 2
	elif not noPrefMatch:
		#print('Can\'t figure out preference???\n\n')
		errors.append("**Preferences doesn't match any of the categories**.\n")

	# Check if keywords for level of preference
	prefMatch = matchFor(field, prefWords, string)
	onlyMatch = matchFor(field, onlyWords, string)
	
	if prefMatch:
		if onlyMatch:
			#print('Included only and preferred??\n\n')
			errors.append("**Preferences match multiple levels**.\n")
		else:
			only = False
	elif not onlyMatch:
		#print('Pref/only not stated???\n\n')
		errors.append("**Preferences doesn't match any of the levels**.\n")

	# Determine preference and return the correct category
	if pref == 0:
		return "No Preference"
	elif pref == 1:
		if only:
			return "Dragon/Feral Art Only"
		return "Dragon/Feral Art Preferred"
	else:
		if only:
			return "Human Art Only"
		return "Human Art Preferred"

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

# Set the number of pages to look through
numOfPages = 1
if len(endPageNums) != 0:
	numOfPages = endPageNums[0]


# Open file for writing the matching input
f = open('submissions.tsv', 'w+')

# Check through every page in the thread, including the last one, since it is not 0 indexed
for page in range(1, int(numOfPages)+1):
	print("\n\t>>> Now scanning page " + str(page) + "/" + str(numOfPages) + "<<<\n")
	# Accessing the new page by adding its number at the end of the thread's url
	pageHTML = requests.get(url + '/' + str(page))
	tree = html.fromstring(pageHTML.content)

	# Get all posts
	posts = tree.xpath(postPath)

	# Remove the first three non-submission posts, if on the first page
	if page == 1:
		posts = posts[3:]

	# This is where each submission is stored for matching
	submissions_match = []

	# i = 0

	# Loop through all submission posts
	for post in posts:
		submission = []
		# For tracking any errors that might arise
		errors = []

		# i+=1
		# if i == 7 and page == 11:
		# 	break;


		postContent = post.xpath(contentPath)
		
		errors.append("----\n")

		# Find the username
		submission.append(getValue('Username:', postContent, errors))

		# Find the id
		submission.append(getValue('ID:', postContent, errors))

		errors.append(submission[0] + ' - ' + submission[1] + '\n')

		# Find the draw preference
		submission.append(determinePref('What kind of art would you prefer to -draw\\?-', postContent, errors))

		# Find the receive preference
		submission.append(determinePref('What kind of art would you prefer to -receive\\?-', postContent, errors))

		# Find backup santa or no
		submission.append(yesOrNo(postContent, errors))

		# Add the link to the post
		submission.append(url + '/' + str(page) + '#' + post.xpath(IDPath))

		errors.append(submission[5] + '\n')

		# Add the submission to the stats array
		submissions_stats.append(submission)

		# Combine submission list into a tab separated string and add it to all submissions
		info = '\t'.join(submission)
		submissions_match.append(info)

		# Write to error log if any errors occur.
		if len(errors) > 3:
			error_log.append('\n'.join(errors))

	# Combine all submissions into a string
	submissionInfo = '\n'.join(submissions_match)
	
	# Store submissions into the file
	f.write(submissionInfo.encode('utf-8') + '\n')

f.close()

# Open file for writing to the directory
f = open('directory.txt', 'w+')

# By Post Order
f.write("[b]By Post Order:[/b]\n" + genDirectoryText(submissions_stats) + "\n\n")

# Alphabetically
f.write("[b]Alphabetical:[/b]\n" + genDirectoryText(alphabeticSort(submissions_stats)) + "\n\n")

# Note, could technically reduce run time by breaking apart the array during filtering
# TODO do something like this or just count to make sure the total matches the number in each category!

# Those who want dragons
f.write("[b]Want Dragon Art:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, "dragon/feral art only", "dragon/feral art preferred"))) + "\n\n")

# Those who want humanoid
f.write("[b]Want Human Art:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, "human art only", "human art preferred"))) + "\n\n")

# Those who don't care
f.write("[b]No Preference for Receiving:[/b]\n" + genDirectoryText(alphabeticSort(filterBy(submissions_stats, "no preference", "no preference"))))

# Stats
f.write('\n\nTotal Participants: [b]' + str(len(submissions_stats)) + '[/b]')

f.close()

# Generating pinglist
f = open ('pinglist.txt', 'w')
f.write(genPinglist(alphabeticSort(submissions_stats)).encode('utf-8') + "\n")
f.close()

# Generating error/exception log
error_log = ''.join(error_log) 
f = open('error_log.txt', 'w')
f.write(error_log)
f.close()