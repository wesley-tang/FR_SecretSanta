import csv
import random
import sys

TAG = ["FR Dragon", "Humanoid", "Anthropomorphic", "Feral"]

santas = []
recips = []

# Open the tsv file for reading
with open(sys.argv[1]) as tsvin:
	tsvin = csv.reader(tsvin, delimiter='\t')

	for row in tsvin:
		santas.append((row[0], row[1], row[2], row[3], row[4]))
		recips.append((row[0], row[1], row[5], row[6], row[7], row[8], row[9]))


origSantas = santas.copy()
origRecip = recips.copy()

stillMatching = True
optimalVal = 35.0

matchups = []
newSantas = []

matchFound = False

while stillMatching:
	for santa in santas:
		# print("Attempting match " + santa[0])

		#If they have no prefer tier, then move up all in willing tier
		if (santa[2] == "none"):
			santa = list(santa)
			santa[2] = santa[3]
			santa = tuple(santa)

		# Attempt to match a santa x times
		iter = 0
		while iter < len(recips):
			if len(recips) == 0:
				break
			for pref in str(santa[2]):
				randomRecip = recips[random.randrange(len(recips))]
				if (santa[0] != randomRecip[0] and float(randomRecip[int(pref)+2]) >= optimalVal):
					#Match made!
					matchString = "Matched because you wanted to draw " + TAG[int(pref)-1] + ", and the recipient has subject(s) with this tag. Confidence: " + str(float(randomRecip[int(pref)+2])) + "/" + str(optimalVal)
					matchups.append((santa[0], santa[1], randomRecip[0], randomRecip[1], randomRecip[2],  matchString, randomRecip[int(pref)+2]))
					recips.remove(randomRecip)
					iter = len(recips)
					matchFound = True
					# print("Match Found")
					# print(randomRecip)
					# print(TAG[int(pref)-1] + "(" + pref  +"): " + randomRecip[int(pref)+2] + "(" + str(int(pref)+2) + ")")
					# print(matchups[len(matchups)-1][0], matchups[len(matchups)-1][2], matchups[len(matchups)-1][5])
					# print("\n")
					break
			iter += 1

		if not matchFound:
			newSantas.append(santa)
			# print("No match found here, adding to the next one...\n")
		matchFound = False

	print("help me")
	print(optimalVal)
	if len(newSantas) > 0:
		optimalVal -= 1
		# print("\nLowered optimal value to: " + str(optimalVal) +"!")
		# print("Matched: " + str(len(santas) - len(newSantas)))
		random.shuffle(newSantas)
		santas = newSantas.copy()
		# print("Left to match: " + str(len(recips)) +"\n")
		newSantas = []
	else:
		stillMatching = False

	if optimalVal < 0:
		# print(santas)
		# print(recips)
		print("\n\n------FAILURE------\n")
		newSantas = []
		optimalVal = 35.0
		santas = origSantas.copy()
		recips = origRecip.copy()
		matchups = []


with open('matchups.tsv', 'a+') as f:
	for match in matchups:
		f.write('\t'.join(match))
		f.write('\n')
	f.close()