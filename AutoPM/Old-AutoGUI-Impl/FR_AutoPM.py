import pyautogui, sys, time, csv
from random import *

# IMPORTANT!!! THE SCREEN MUST BE ORIENTED SO THAT THE WEBPAGE IS AT ITS MIN SIZE

print('Press Ctrl-C to quit.')

pyautogui.FAILSAFE = True


try:
	# Open the tsv file for reading
	with open('matchups.tsv', newline='') as tsvin:
		tsvin = csv.reader(tsvin, delimiter='\t')
		# 0: Artist name, 1: Recipient Page, 2: Recipient name
		# 3: Recipient Rec Pref, 4: Recipient References
		for row in tsvin:
			if row[0] == "Hexlash":
				with open('hex.txt', 'w') as f:
					message = 'Greetings {}, thank you very much for participating in our 2018 Secret Santa Art Trade event!\n\nThis year, you have been assigned to draw art for [url={}]{}[/url]. Their art preference was [b]{}[/b], and this is the info on the characters/dragons they would like drawn:\n\n[quote]\n{}\n[/quote]\n\nIf you have any additional questions for your recipient, let us know so we can pass on your question to them while keeping your identity a secret. :)\n\nPlease remember to submit your artwork to us before [b]December the 23rd at rollover,[/b] so we can have the main post updated with all of the art by Christmas Day.\n\nAs a reminder, please let us know if you change your username at any point during this event. If something comes up and you know you won\'t be able to finish your artwork on time, please notify one of us ASAP and we will do our best to make sure that the recipient you were originally assigned to will receive artwork by Christmas.\n\nThat\'s all for now! If you have any more questions about the event in general, feel free to ask.\n\nWe look forward to seeing your artwork! :)'
					message = message.format(row[0], row[1] ,row[2], row[3], row[4])

					f.write(message)
					f.close()
			else:
				# Go to the PM page
				#print('Going to new PM page')
				pyautogui.moveTo(300, 75)
				pyautogui.click()

				# Inserting the proper link to PM the user
				link = 'www1.flightrising.com/msgs/new?to=' + row[0]

				#print('\n' + link)
				pyautogui.typewrite(link)
				pyautogui.press('enter')
				temp = None
				while temp == None:
					temp = pyautogui.locateOnScreen('loaded.png')
				time.sleep(0.4)

				# Enter Subject
				#print('Entering subject')
				pyautogui.moveTo(345, 488)
				time.sleep(0.2)
				pyautogui.click()

				pyautogui.typewrite('FR Secret Santa Art Trade Recipient')

				# Send the message

				# Constructing message
				message = 'Greetings {}, thank you very much for participating in our 2018 Secret Santa Art Trade event!\n\nThis year, you have been assigned to draw art for [url={}]{}[/url]. Their art preference was [b]{}[/b], and this is the link to their entry:\n\n[quote]\n{}\n[/quote]\n\nIf you have any additional questions for your recipient, let us know so we can pass on your question to them while keeping your identity a secret. :)\n\nPlease remember to submit your artwork to us using [url=https://docs.google.com/forms/d/e/1FAIpQLSfZWnbsrX8EVA57TzXzV492jmwochAm_MLcP_Gqio6y-UcXTQ/viewform]this form[/url] before [b]December the 23rd at rollover,[/b] so we can have the main post updated with all of the art by Christmas Day.\n\nAs a reminder, please let us know if you change your username at any point during this event. If something comes up and you know you won\'t be able to finish your artwork on time, please notify one of us ASAP and we will do our best to make sure that the recipient you were originally assigned to will receive artwork by Christmas.\n\nThat\'s all for now! If you have any more questions about the event in general, feel free to ask.\n\nWe look forward to seeing your artwork! :)'
				message = message.format(row[0], row[1] ,row[2], row[3], row[4]).replace("\\n", chr(10))
				
				messageCut = message
				while len(message) > 0:
					messageCut = (message[:1500])
					print( '                   $$$' + messageCut + '&&&' )
					message = message[1500:]
					time.sleep(0.08)

					textStart = pyautogui.locateOnScreen('start.png')
					textEnd = pyautogui.locateOnScreen('end.png', region=(930, 45, 495, 770))

					#print(textStart)
					#print(textEnd)

					if textStart == None or textEnd == None:
						pyautogui.moveTo(1000, 60)
						pyautogui.click()
						pyautogui.typewrite('clear')
						pyautogui.press('enter')

						pyautogui.moveTo(370, 580)
						pyautogui.doubleClick()
						pyautogui.hotkey('command', 'down')
						time.sleep(0.05)
						pyautogui.typewrite(messageCut)
					else:
						pyautogui.moveTo(textStart[0]+29, textStart[1])
						pyautogui.click()
						pyautogui.dragTo(textEnd[0], textEnd[1]+10, button='left')
						pyautogui.hotkey('command', 'c')
						pyautogui.typewrite('clear')
						pyautogui.press('enter')
						# Enter Message body
						#print('Entering body')
						pyautogui.moveTo(370, 580)
						pyautogui.doubleClick()
						pyautogui.hotkey('command', 'down')
						time.sleep(0.05)
						pyautogui.hotkey('command', 'v')
				#print('Sending message')
				pyautogui.moveTo(760, 753)
				pyautogui.click()
				#print('waiting...')
				#time.sleep(2.5)
				temp = None
				while temp == None:
					#pyautogui.moveTo(760, 753)
					#pyautogui.click()
					temp = pyautogui.locateOnScreen('sent.png')
				time.sleep(0.4)


except KeyboardInterrupt:
    print('\n')