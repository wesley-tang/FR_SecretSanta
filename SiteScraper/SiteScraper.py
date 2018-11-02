# Imports required libraries
from lxml import html
import requests

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

# Open file for writing
f = open('submissions.tsv', 'w+')

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

	# This is where each submission is stored
	submissions = []

	# Loop through all submission posts
	for post in posts:
		submission = []
		# Skip the white spaces and only grab what we need while also trimming LEFT whitespace
		for i in range(1,10,2):
			submission.append(post.xpath(contentPath)[i].lstrip())
		# TODO Add error trap???

		# Add the link to the post
		submission.append(url + '/' + str(page) + '#' + post.xpath(IDPath))

		# Combine submission list into a string and add it to all submissions
		info = '\t'.join(submission)
		submissions.append(info)
	
	# Combine all submissions into a string
	submissionInfo = '\n'.join(submissions)
	
	# Store submissions into the file
	f.write(submissionInfo.encode('utf-8'))
	
f.close()
