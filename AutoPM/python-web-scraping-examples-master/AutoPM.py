from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import secrets

# URLs
SIGNIN_URL= 'https://www1.flightrising.com/login'
PM_URL= 'https://www1.flightrising.com/msgs/new?to='

continueSending = True

# Open the tsv file for reading
with open('matchups.tsv') as tsvin:
	# 0: Artist name, 1: Recipient Page, 2: Recipient name
	#3: Recipient References
	tsvin = csv.reader(tsvin, delimiter='\t')

	opts = Options()
	opts.set_headless()
	browser = Chrome(options=opts)

	#Go to FR's sign in page
	browser.get(SIGNIN_URL)

	#Sign into FR
	username_form = browser.find_element_by_id('uname')
	password_form = browser.find_element_by_id('pword')
	username_form.send_keys(secrets.username)
	password_form.send_keys(secrets.password)
	submit_button = browser.find_element_by_id('big-login-form-button')
	submit_button.click()

	for row in tsvin:
		if continueSending:
			if row[0] == "Hexlash":
				with open('hex.txt', 'w') as f:
					message = 'Greetings {}, thank you very much for participating in our 2019 Secret Santa Art Trade event!\n\nThis year, you have been assigned to draw art for [url={}]{}[/url]. Their sign-up form with the subjects they would like drawn is here:\n\n[quote]\n{}\n[/quote]\n\nIf you have any additional questions for your recipient, let us know so we can pass on your question to them while keeping your identity a secret. :)\n\nPlease remember to submit your artwork to us before [b]December the 23rd at rollover,[/b] so we can have the main post updated with all of the art by Christmas Day.\n\nAs a reminder, please let us know if you change your username at any point during this event. If something comes up and you know you won\'t be able to finish your artwork on time, please notify one of us ASAP and we will do our best to make sure that the recipient you were originally assigned to will receive artwork by Christmas.\n\n[b]If you have any questions, please don\'t reply directly to this message as I will be unable to respond as the matchups are sent out.[/b]\n\nThat\'s all for now! If you have any more questions about the event in general, feel free to ask.\n\nWe look forward to seeing your artwork! :)'
					message = message.format(row[0], row[1] ,row[2], row[3])

					f.write(message)
					f.close()
			else:
				print("Started " + row[0])
				# Going to PM page for user
				browser.get(PM_URL + row[0])

				subject_form = browser.find_element_by_name('subject')
				subject_form.send_keys('FR Secret Santa Art Trade Recipient')

				# Constructing message
				message = 'Greetings {}, thank you very much for participating in our 2019 Secret Santa Art Trade event!\n\nThis year, you have been assigned to draw art for [url={}]{}[/url]. Their sign-up form with the subjects they would like drawn is here:\n\n[quote]\n{}\n[/quote]\n\nIf you have any additional questions for your recipient, let us know so we can pass on your question to them while keeping your identity a secret. :)\n\nPlease remember to submit your artwork to us before [b]December the 23rd at rollover,[/b] so we can have the main post updated with all of the art by Christmas Day.\n\nAs a reminder, please let us know if you change your username at any point during this event. If something comes up and you know you won\'t be able to finish your artwork on time, please notify one of us ASAP and we will do our best to make sure that the recipient you were originally assigned to will receive artwork by Christmas.\n\n[b]If you have any questions, please don\'t reply directly to this message as I will be unable to respond as the matchups are sent out.[/b]\n\nThat\'s all for now! If you have any more questions about the event in general, feel free to ask.\n\nWe look forward to seeing your artwork! :)'
				message = message.format(row[0], row[1] ,row[2], row[3]).replace("\\n", chr(10))
				
				message_form = browser.find_element_by_id('message')
				message_form.send_keys(message)

				# Send the message
				send_button = browser.find_element_by_id('submit-reply')
				send_button.click()
				
				#Confirm success
				try:
					confirmation = browser.find_element_by_id('sent-confirm')
					if "Your message has been delivered." not in confirmation.text:
						raise Exception("Message failed to deliver.")
				except:
					print('Unable to find confirmation, stopping here.')
					continueSending = False

					with open('remainingMatchups.tsv', 'w+') as f:
						f.write('\t'.join(row))
						f.close()
			print("Done one")

		else:
			# On a failure, write the leftover matchups
			with open('remainingMatchups.tsv', 'a+') as f:
				f.write('\t'.join(row))
				f.close()

	browser.close()
	print('done!')