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

USERNAME = 0
USERID = 1
PREFER = 2
WILLING = 3
BANNED = 4
LINK = 5
SUBJECT_DRAG = 6
SUBJECT_HUMAN = 7
SUBJECT_ANTHRO = 8
SUBJECT_FERAL = 9
BACKUP = 10
TIER = 11

# ---- NEED TO UPDATE EVERY YEAR -----

# Set the number of pages to look through
numOfPages = 1
# Initial posts to skip
numInitialPosts = 2
# URL to search for submission posts
url = 'https://www1.flightrising.com/forums/cc/3079245'

# -------------------------------------

subjectName = "Subject Name:"

# Error log to track any oddities or problems
error_log = []

# Retrieves HTML from a given URL and stores it in an organized tree
page = requests.get(url)
tree = html.fromstring(page.content)

# The path to find the max number of pages in the thread
# Looks for the div where the navigable page numbers are held and finds the last one
pageNumPath = 'string(//div[@class=\'common-pagination-pages\']/a[last()])'
# Path for the posts
postPath = '//div[@class=\'post  \' or @class=\'post   no-signature \']'
# Get the string value of the post's ID to get its direct link
IDPath = 'string(./@id)'
# Path to the content of the post, looking only at plain text
contentPath = 'string(.//div[@class=\'post-text-content\'])'
# Path to the author
authorPathUrl = 'string(.//a[@class=\'post-author-username\']/@href)'
authorPathName = 'string(.//a[@class=\'post-author-username\'])'

userIdRegex = 'https:\/\/www1\.flightrising\.com\/clan-profile\/(\d+)'
codeRegex = '~\/(?:p(\d+))?(?:w(\d+))?(?:b(\d+))?S(.*)St(\d)s(\d)\/~'
subjectRegex = '(?:n|r(\d))T(\d+)'



# This is where all submissions are stored for stats
submissions_stats = []
subjects_stats = []

# Takes a list of submissions and returns a string directory from it, encoded
def genDirectoryText(submissions):
	text = ""
	# Loop through all submissions in the list and generate the directory
	for sub in submissions:
		text += ("[url=" + sub[LINK] + "]" + sub[USERNAME] + "[/url]" + " " + u'\u2022' + " ")
	# Return the resulting string minus the extra bullet at the end
	return text[:-3].encode('utf-8')

# Sorts and returns the list
def alphabeticSort(list):
	return sorted(list, key=lambda s: s[0].lower())

# Takes submissions and filters them by the index corresponding to the specified value
def filterBy(subjects, restriction):
	newSubjects = []
	# Check all submissions and only include those that match
	# either the highest preference of the receive, or the tier
	for sub in subjects:
		if restriction in sub[1]:
			newSubjects.append(sub)
	return newSubjects

def genSubjectDirectory(subjects):
	text = ""
	for sub in subjects:
		text += ("[url=" + sub[2] + "]" + sub[0] + "[/url]" + " " + u'\u2022' + " ")
	# Return the resulting string minus the extra bullet at the end
	return text[:-3].encode('utf-8')


# Takes list of submissions and creates the pinglist for it
def genPinglist(submissions):
	text = ""
	for sub in submissions:
		text += "@" + sub[0] + " "
	return text

def getSubjects(subjectCode, subjectNames, subjects, submission):
	subjectVal = [0.0, 0.0, 0.0, 0.0]

	rankedPoints = [18, 9, 4, 2, 1]

	
	subjectMatches = re.findall('(?:n|r(\d))T(\d+)', subjectCode)
	for subject, subjectName in zip(subjectMatches, subjectNames):

		subjects.append((subjectName, subject[1], submission[LINK]))

		for tag in str(subject[1]):
			if subject[0]:
				subjectVal[int(tag)-1] += rankedPoints[int(subject[0])]
			else:
				subjectVal[int(tag)-1] += 6.8
			
	for val in subjectVal:
		submission.append(str(val))




# Find the el\ement according to the path
endPageNums = tree.xpath(pageNumPath)
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

	for post in posts:
		# 0 - username
		# 1 - user id
		# 2 - prefer drawing
		# 3 - willing to draw
		# 4 - will not draw
		# 5 - subject fr drag val
		# 6 - subject fr human val
		# 7 - subject fr anthro val
		# 8 - subject fr feral val
		# 9 - backup santa
		# 10 - link to post
		# 11  - tier (1 = A, 0 = B)
		submission = []
		subjects = []
		errors = []		
		errors.append("----\n")


		userId = re.search(userIdRegex, post.xpath(authorPathUrl)).group(1)
		username = post.xpath(authorPathName)


		submission.append(username)
		submission.append(userId)


		postContent = post.xpath(contentPath)
		codeMatch = re.search(codeRegex, postContent)


		# Draw prefs
		submission.append(str(codeMatch.group(1) if codeMatch.group(1) else "none" ))
		submission.append(str(codeMatch.group(2) if codeMatch.group(2) else "none" ))
		submission.append(str(codeMatch.group(3) if codeMatch.group(3) else "none" ))


		# Add the link to the post
		submission.append(url + '/' + str(page) + '#' + post.xpath(IDPath))

		# Subjects
		subjectsCode = codeMatch.group(4)
		subjectNames = re.findall('Subject Name: *(\S*)', postContent)
		getSubjects(subjectsCode, subjectNames, subjects, submission)

		submission.append(codeMatch.group(6)) #out of order to put tier last

		# TIER
		submission.append(codeMatch.group(5))


		submissions_stats.append(submission)
		subjects_stats += subjects


		info = '\t'.join(submission[:-1])
		# print(info)

		if submission[TIER] == '1':
			signupsTierA.append(info)
		elif submission[TIER] == '0':
			signupsTierB.append(info)
		else:
			errors.append("Could not determine Tier (default to B)")
			signupsTierB.append(info)


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


f.write('[b][size=4]PARTICIPANTS:[/size][/b]\n\n')

f.write("[b]By Post Order:[/b]\n" + genDirectoryText(submissions_stats) + "\n\n")

f.write("[b]Alphabetical:[/b]\n" + genDirectoryText(alphabeticSort(submissions_stats)) + "\n\n")

f.write('Total Participants: [b]' + str(len(submissions_stats)) + '[/b]\n\n')


f.write('\n[b][size=4]SUBJECTS:[/size][/b]\n\n')

f.write("[b]Dragon Subjects:[/b]\n" + genSubjectDirectory(alphabeticSort(filterBy(subjects_stats, '1'))) + "\n\n")

f.write("[b]Humanoid Subjects:[/b]\n" + genSubjectDirectory(alphabeticSort(filterBy(subjects_stats, '2'))) + "\n\n")

f.write("[b]Anthropomorphic Subjects:[/b]\n" + genSubjectDirectory(alphabeticSort(filterBy(subjects_stats, '3'))) + "\n\n")

f.write("[b]Feral Subjects:[/b]\n" + genSubjectDirectory(alphabeticSort(filterBy(subjects_stats, '4'))) + "\n\n")

# Stats
f.write('\nTotal Subjects: [b]' + str(len(subjects_stats)) + '[/b]')

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
