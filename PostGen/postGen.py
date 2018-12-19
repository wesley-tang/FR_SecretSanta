import csv, requests

formatString = "\n[columns]\n[url={}][img]{}[/img][/url]\n[nextcol]\n[img]https://i.imgur.com/lPELxya.png[/img]\n[nextcol]\n[center]\n\n{}\n\nFor @{}\nDrawn by {}\n[/center]\n[/columns]\n[center][img]https://s2.postimg.cc/xgqe33p0p/Divider-640.png[/img][/center]\n"

#Timestamp	What is YOUR OWN username?	What is YOUR RECIPIENT'S username?	Is this a primary or secondary recipient?	Paste the link to your artwork here:	Did you draw Dragon/Feral art or Human/Gijinka/Humanoid/Anthro art?	(optional) A little message for your recipient! [max 300 characters]	(optional) Anything you would like the organizers to know!	Would you like to be pinged when we host this event next year?	Thumbnail IMG
feralArts = []
humanArts = []

# Sorts and returns the list
def alphabeticSort(list):
	return sorted(list, key=lambda s: s[1].lower())

# Generate art post by writing to the file using the given list
def artPostGen(list, f):
	f.write("\n[center][img]https://s2.postimg.cc/xgqe33p0p/Divider-640.png[/img]\n[/center]");
	for art in list:
		# first image url, then thumbnail url, message, recip, artist,
		submission = formatString.format(art[2], art[4], art[3], art[1], art[0])

		f.write(submission)
	f.close()

# Open the tsv file for reading
with open('ART SUBMISSIONS - Form Responses 1.tsv', 'r') as tsvin:
	tsvin = csv.reader(tsvin, delimiter='\t')

	# 0:artist, 1:recip, 2:link to art 3:message, 4:thumbnail
	for row in tsvin:
		# Accounting for anonymous people
		if row[1] == "(anonymous)":
			artist = "[i]anonymous[/i]"
		else:
			artist = "@" + row[1]

		# Will ignore invalid first row which does not contain either category
		# Sort the art into their appropriate sections
		if row[5] == "Dragon/Feral":
			feralArts.append([artist, row[2], row[4], row[6], row[9]])
		elif row[5] == "Human/Gijinka/Humanoid/Anthro":
			humanArts.append([artist, row[2], row[4], row[6], row[9]])

# Sort by recipient
feralArts = alphabeticSort(feralArts)
humanArts = alphabeticSort(humanArts)

print("Doing ferals! :3c")
with open('feralPost.txt', 'w+') as f:
	artPostGen(feralArts, f)
	f.close()

print("Doing humans! :Dc")
with open('humanPost.txt', 'w+') as f:
	artPostGen(humanArts, f)
	f.close()

print("All done! ^w^")