# Imports required libraries
from lxml import html
import requests

# Note: sub[0]: name, sub[1]: id#, sub[2]: want to draw,
# sub[3]: want to receive, sub[4]: backup santa or not, sub[5]: post link

# Takes a list of submissions and returns a string directory from it
def genDirectoryText(submissions):
	text = ""
	# Loop through all submissions in the list and generate the directory
	for sub in submissions:
		text += ("[url=" + sub[5] + "]" + sub[0] + "[/url]" + " " + u'\u2022' + " ")
	# Return the resulting string minus the extra bullet at the end
	return text[:-3]

# Takes submissions and filters them by what the submitter wants drawn
def filterBy(submissions, restric1, restric2):
	newSubmissions = []
	# Check all submissions and only include those that match the criteria.
	for sub in submissions:
		if sub[3].lower() == restric1 or sub[3].lower() == restric2:
			newSubmissions.append(sub)
	return newSubmissions

# URL to search for submission posts
url = 'http://www1.flightrising.com/forums/cc/2554259'

# Retrieves HTML from a given URL and stores it in an organized tree
page = requests.get(url)
tree = html.fromstring(page.content)

# The path to find the max number of pages in the thread
# Looks for the div where the navigable page numbers are held and finds the last one
pageNumPath = '//div[@class=\'common-pagination-numbers\']/a[last()]/text()'
# Path for the posts
postPath = '//div[@class=\'post \']'
# Get the string value of the post's ID to get its direct link
IDPath = 'string(./@id)'
# Path to the content of the post, loking only at plain text
contentPath = './/div[@class=\'post-text-content\']/text()'

# Find the element according to the path
endPageNums = tree.xpath(pageNumPath)

# Set the number of pages to look through
numOfPages = 1
if len(endPageNums) != 0:
	numOfPages = endPageNums[0]

# Check through every page in the thread, including the last one, since it is not 0 indexed
for page in range(1, numOfPages+1):
	print("Now scanning page " + str(page) + "/" + str(numOfPages))
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

	# This is where all submissions are stored for stats
	submissions_stats = []

	# Loop through all submission posts
	for post in posts:
		submission = []
		# Skip the white spaces and only grab what we need while also trimming LEFT whitespace
		for i in range(1,10,2):
			submission.append(post.xpath(contentPath)[i].lstrip())
		# TODO Add error trap???
		# somestring.lower()

		# Add the link to the post
		submission.append(url + '/' + str(page) + '#' + post.xpath(IDPath))

		# Add the submission to the stats array
		submissions_stats.append(submission)

		# Combine submission list into a tab separated string and add it to all submissions
		info = '\t'.join(submission)
		submissions_match.append(info)


	# Open file for writing the matching input
	f = open('submissions.tsv', 'w+')

	# Combine all submissions into a string
	submissionInfo = '\n'.join(submissions_match)
	
	# Store submissions into the file
	f.write(submissionInfo.encode('utf-8'))

# Open file for writing to the directory
f = open('directory.txt', 'w+')

# By Post Order
f.write("[b]By Post Order:[/b]\n" + genDirectoryText(submissions_stats).encode('utf-8') + "\n\n")

# Alphabetically
f.write("[b]Alphabetical:[/b]\n" + genDirectoryText(sorted(submissions_stats)).encode('utf-8') + "\n\n")

# Those who want dragons
f.write("[b]Want Dragon Art:[/b]\n" + genDirectoryText(filterBy(submissions_stats, "dragon/feral art only", "dragon/feral art preferred")).encode('utf-8') + "\n\n")

# Note, could technically reduce run time by breaking apart the array during filtering

# Those who want humanoid
f.write("[b]Want Human Art:[/b]\n" + genDirectoryText(filterBy(submissions_stats, "human art only", "human art preferred")).encode('utf-8') + "\n\n")

# Those who don't care
f.write("[b]No Preference:[/b]\n" + genDirectoryText(filterBy(submissions_stats, "no preference", "no preference")).encode('utf-8'))

f.close()
