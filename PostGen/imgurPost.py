import csv, requests

#Timestamp	What is YOUR OWN username?	What is YOUR RECIPIENT'S username?	Is this a primary or secondary recipient?	Paste the link to your artwork here:	Did you draw Dragon/Feral art or Human/Gijinka/Humanoid/Anthro art?	(optional) A little message for your recipient! [max 300 characters]	(optional) Anything you would like the organizers to know!	Would you like to be pinged when we host this event next year?	Thumbnail IMG
feralArts = []
humanArts = []

# Upload all images to an imgur album
url = "https://api.imgur.com/3/image"

# Album IDs
feralAlbum = "IC2mp0PgTfILBry"
humanAlbum = "h9p85XgrCa8vePB"

# First is image URL, then title, description, then title name
payloadFormat = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"album\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"description\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

# For auth
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'Authorization': "Client-ID 02ab23daa6a03ea",
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "afb5527f-f2da-41b4-8481-f1115c5b9636"
    }

# Sorts and returns the list
def alphabeticSort(list):
	return sorted(list, key=lambda s: s[1].lower())

# Take the given list of art, the album deletehash and the filename in case of failure and upload images to imgur
def uploadImages(arts, album, fileName):
	onIndex = 0

	if len(arts) == 0:
		print("Already finished all feral art!\n")
		return True

	for art in arts:
		payload = payloadFormat.format(art[2], album, ("For " + art[1] + ", Drawn by " + art[0]), art[3], art[0])
		response = requests.request("POST", url, data=payload, headers=headers)

		responseJSON = response.json()

		if not responseJSON['success']:
			if responseJSON['data']['error']['code'] == 1003:
				print("Submission type failed! Manual uploading necessary?\n")
				print("\t > " + art[2] + "\n")
			elif responseJSON['data']['error']['code'] == 429:
				print("Hit submission limit for this hour! >:c\nUpdating " + fileName + " with list of submissions still left...")

				newArts = arts[onIndex:len(arts)]

				# Open file for writing new file
				entries = []
				f = open(fileName, 'w')
				for newArt in newArts:
					entries.append(newArt[0] + "\t" + newArt[1] + "\t" + newArt[2] + "\t" + newArt[3] + "\t" + newArt[4])
				f.write('\n'.join(entries))
				f.close()

				print("Submissions have been updated.")

				return False
			else:
				print("\nOther error occured!!!")
				print("\t > " + response.text + "\n")
		else:
			print("Done " + art[0] + "'s!" + " (" + str(onIndex+1) + "/" + str(len(arts)) + ")\n")
		onIndex += 1
	return True

#Try opening edited tsv
try:
	with open('feralArt.tsv', 'r') as tsvin:
		print("Picking up from last time!")
		tsvin = csv.reader(tsvin, delimiter='\t')

		# 0:artist, 1:recip, 2:link to art 3:message, 4:thumbnail
		for row in tsvin:
			if row[0] == "done":
				print("Feral art is already done.")
				break
			feralArts.append([row[0], row[1], row[2], row[3], row[4]])

	with open('humanArt.tsv', 'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')

		# 0:artist, 1:recip, 2:link to art 3:message, 4:thumbnail
		for row in tsvin:
			humanArts.append([row[0], row[1], row[2], row[3], row[4]])

except IOError:
	print("Updated art submission data not found, relying on the original. If the updated ones exist, then double uploading is happeneing! Please STOP immediately!")
	# Open the tsv file for reading
	with open('ART SUBMISSIONS - Form Responses 1.tsv', 'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')

		# 0:artist, 1:recip, 2:link to art 3:message, 4:thumbnail
		for row in tsvin:
			# Accounting for anonymous people
			if row[1] == "(anonymous)":
				artist = "anonymous"
			else:
				artist = row[1]

			# Will ignore invalid first row which does not contain either category
			# Sort the art into their appropriate sections
			if row[5] == "Dragon/Feral":
				feralArts.append([artist, row[2], row[4], row[6], row[9]])
			elif row[5] == "Human/Gijinka/Humanoid/Anthro":
				humanArts.append([artist, row[2], row[4], row[6], row[9]])

# Sort by recipient
feralArts = alphabeticSort(feralArts)
humanArts = alphabeticSort(humanArts)


print("\n~~~~~~~~~~~~~~~\nPosting feral art to imgur...\n ~~~~~~~~~~~~~~~")

if uploadImages(feralArts, feralAlbum, "feralArt.tsv"):
	print("Completed feral art!\n")
	f = open("feralArt.tsv", 'w+')
	f.write("done")
	f.close()
else:
	print("Not completed feral art!\n")

print("\n~~~~~~~~~~~~~~~\nDone feral art\nPosting human art to imgur...\n ~~~~~~~~~~~~~~~\n")

if uploadImages(humanArts, humanAlbum, "humanArt.tsv"):
	print("Completed human art!")
else:
	print("Not completed human art!")
	
