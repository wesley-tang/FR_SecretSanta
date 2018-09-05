# Gets the artist's recipient
import csv

# Search through file
def findRecip():
	with open('matchups.tsv', newline='') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		for row in tsvin:
			if row[0] == artist:
				print('The recipient is: ' + row[2])
				return True
	return False

# Get artist to find recipient for
artist = input('Enter the Secret Santa Artists name to get their recipient: ')

if not findRecip():
	print('Could not match this person to anyone.')

