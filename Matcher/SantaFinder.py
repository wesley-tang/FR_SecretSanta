# Gets the artist's recipient
import csv

# Search through file
def findRecip():
	with open('matchups.tsv', newline='') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		for row in tsvin:
			if row[2] == recip:
				print('The recipient is: ' + row[0])
				return True
	return False

# Get artist to find recipient for
recip = input('Enter the Recipient name to get their artist: ')

if not findRecip():
	print('Could not match this person to anyone.')

