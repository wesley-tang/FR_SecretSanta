import pyautogui, sys, time, csv
from random import *

# IMPORTANT!!! THE SCREEN MUST BE ORIENTED SO THAT THE WEBPAGE IS AT ITS MIN SIZE


# Open the tsv file for reading
with open('matchups.tsv', newline='') as tsvin:
	tsvin = csv.reader(tsvin, delimiter='\t')
	# 0: Artist name, 1: Recipient Page, 2: Recipient name
	# 3: Recipient Rec Pref, 4: Recipient References

	with open('matchupsLeft.txt', 'w+') as f:
		i = 0
		for row in tsvin:
			i+=1
			# Inserting the proper link to PM the user
			link = 'www1.flightrising.com/msgs/new?to=' + row[0]

			#print('\n' + link)
			f.write(link + "\n")

			message = 'Greetings {}, thank you very much for participating in our 2018 Secret Santa Art Trade event!\n\nThis year, you have been assigned to draw art for [url={}]{}[/url]. Their art preference was [b]{}[/b], and this is the link to their entry:\n\n[quote]\n{}\n[/quote]\n\nIf you have any additional questions for your recipient, let us know so we can pass on your question to them while keeping your identity a secret. :)\n\nPlease remember to submit your artwork to us using [url=https://docs.google.com/forms/d/e/1FAIpQLSfZWnbsrX8EVA57TzXzV492jmwochAm_MLcP_Gqio6y-UcXTQ/viewform]this form[/url] before [b]December the 23rd at rollover,[/b] so we can have the main post updated with all of the art by Christmas Day.\n\nAs a reminder, please let us know if you change your username at any point during this event. If something comes up and you know you won\'t be able to finish your artwork on time, please notify one of us ASAP and we will do our best to make sure that the recipient you were originally assigned to will receive artwork by Christmas.\n\nThat\'s all for now! If you have any more questions about the event in general, feel free to ask.\n\nWe look forward to seeing your artwork! :)'
			message = message.format(row[0], row[1] ,row[2], row[3], row[4]).replace("\\n", chr(10))
			
			f.write(message)

			f.write("\n\n--------------------------------------------------\n\n")
		f.close()
		print(i)

			
