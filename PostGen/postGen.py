import csv, http.client, json

#Timestamp	What is YOUR OWN username?	What is YOUR RECIPIENT'S username?	Is this a primary or secondary recipient?	Paste the link to your artwork here:	Did you draw Dragon/Feral art or Human/Gijinka/Humanoid/Anthro art?	(optional) A little message for your recipient! [max 300 characters]	(optional) Anything you would like the organizers to know!	Would you like to be pinged when we host this event next year?	Thumbnail IMG
feralArts = []
humanArts = []

conn = http.client.HTTPConnection("api,imgur,com")

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

def uploadImages(arts, album, fileName):
	onIndex = 0

	for art in arts:
		payload = payloadFormat.format(art[2], album, ("For " + art[1] + ", Drawn by " + art[0]), art[3], art[0])
		conn.request("POST", "3,image", payload, headers)

		res = conn.getresponse()
		data = res.read().decode('utf-8')
		responseJSON = json.loads(data)

		if not responseJSON['success']:
			if responseJSON['data']['error'] == "1003":
				print("Submission type failed! Manual uploading necessary?\n")
				print("\t > " + art[2] + "\n")
			elif responseJSON['data']['error'] == "429":
				print("Hit submission limit for this hour! >:c\nUpdating list of submissions...")

				newArts = arts[onIndex:len(arts)]

				# Open file for writing new file
				f = open(fileName, 'w+')
				for newArt in newArts:
					f.write(newArt[0] + "\t" + newArt[1] + "\t" + newArt[2] + "\t" + newArt[3] + "\t" + newArt[4] + "\n")
				f.close()

				return
			else:
				print("Other error occured!!!")
				print("\t > " + responseJSON['data']['error'] + "\n")
		else:
			onIndex += 1
			print("Done " + art[0] + "'s!\n" + " (" + str(onIndex) + ")")
			print(response.text)

#Try opening edited tsv
try:
	with open('feralArt.tsv', 'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')

		# 0:artist, 1:recip, 2:link to art 3:message, 4:thumbnail
		for row in tsvin:
			feralArts.append([row[0], row[1], row[2], row[3], row[4]])


	with open('humanArt.tsv', 'r') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')

		# 0:artist, 1:recip, 2:link to art 3:message, 4:thumbnail
		for row in tsvin:
			humanArts.append([row[0], row[1], row[2], row[3], row[4]])

except FileNotFoundError:
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

uploadImages(feralArts, feralAlbum, "feralArt.tsv")

print("\n~~~~~~~~~~~~~~~\nDone feral art\nPosting human art to imgur...\n ~~~~~~~~~~~~~~~")

uploadImages(humanArts, humanAlbum, "humanArt.tsv")

print("Completed!")