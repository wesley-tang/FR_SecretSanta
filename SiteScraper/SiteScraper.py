# Imports required libraries
from lxml import html
import requests

url = 'http://www1.flightrising.com/forums/cc/2306886'

# Retrieves HTML from a given URL and stores it in an organized tree
page = requests.get(url)
tree = html.fromstring(page.content)

# The path to find the max number of pages in the thread
# Looks for the div where the navigable page numbers are held and finds the last one
pageNumPath = '//div[@class=\'common-pagination-numbers\']/a[last()]/text()'
# Path for the posts
postPath = '//div[@class=\'post-text-content\']/text()'

# Find the element according to the path
endPageNums = tree.xpath(pageNumPath)

# Set the number of pages to look through
numOfPages = 0
if len(endPageNums) != 0:
	numOfPages = endPageNums[0]


f = open('text.txt', 'w+')

# Check through every page in the thread, including the last one, since it is not 0 indexed
for page in range(1, int(numOfPages)+1):
	# Accessing the new page by adding its number at the end of the thread's url
	page = requests.get(url + '/' + str(page))
	tree = html.fromstring(page.content)

	# Get all post content
	postsContent = tree.xpath(postPath)
	
	message = '\n\n'.join(postsContent)

	f.write(message.encode('utf-8') + '\n\n')
	
f.close()