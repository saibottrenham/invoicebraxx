"""
Invoicing script
Author: Tobias Mahnert
Date: 10.06.2018
"""
from __future__ import print_function
from apiclient import discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials as SAC
import pandas as pd
import datetime
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.application import MIMEApplication
import codecs
import glob
import smtplib
import os


def createInvoiceFolders(date):
	if not os.path.exists(date):
		os.makedirs(date)


def appendReq(key, value):
	reqs.append({'replaceAllText': {'containsText': {'text': "{{"+key+"}}"},
                            'replaceText': str(value)
                            }})
	return


def getTheInfo(csv, col, nickName):
	df = pd.read_csv(csv)
	info = df.loc[df[col] == nickName].to_dict(orient='records')
	for key, value in info[0].iteritems():
		if key in varsDict:
			varsDict[key] = value
		appendReq(key, value)
	return	


def attachEmailImages(image, imgref):
	fp = open(image, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()
	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<'+imgref+'>')
	msgRoot.attach(msgImage)

def getValues(selectedCSV, selectedColumn):
	clientsDF = pd.read_csv(selectedCSV)
	valuesList = clientsDF[selectedColumn].tolist()
	return valuesList


def printFunction(valuesList):
	print('Select from the options below:\n')
	for i in valuesList:
		print(i)
	print('\n')
	return


def untilValidInput(valuesList, prompt):
	printFunction(valuesList)
	while True:
		userInput = raw_input(prompt)
		if userInput in valuesList:
			return userInput 


start_date = datetime.datetime.today()
end_date = start_date + datetime.timedelta(days=7)


# load the UserInput
reqs = []

# get nickname out of a list of available nicknames
clientsList = getValues('exampleCSV/mydataExample.csv', 'myNickName')
myNickName = untilValidInput(clientsList, 'Please Select Your NickName: ')

# get Clientsname from list of available usernames
clientsList = getValues('exampleCSV/clientsExample.csv', 'cleintNickName')
clientNickname = untilValidInput(clientsList, 'Please Select Clients Name: ')

# get the rest of the vars
rate = float(raw_input('What is your Rate? Please only Numbers: '))
qty = float(raw_input('What is your QTY? Please only Numbers: '))
item = raw_input('What kind of Work?: ')


# get latest invoive NO and append a new one
invoiceDF = pd.read_csv('exampleCSV/invoiceNOExample.csv')
latestNO = invoiceDF['invoiceNO'].tail(1)
latestInvoice = latestNO[len(invoiceDF)-1]
newInvoice = latestInvoice + 10
df2 = pd.DataFrame([newInvoice], columns=list(['invoiceNO']))
invoiceDF = invoiceDF.append(df2)


month = start_date.strftime('%m')
year = start_date.strftime('%Y')


varsDict = {'clientName' : '',
			'myName' : '',
			'myEmail' : '',
			'clientEmail' : '',
			'preferredTemplate' : '',
			'host' : '',
			'port' : '',
			'username' : '',
			'password' : ''}


createInvoiceFolders('invoices/' + year + '/' + month)


# append the newInvoice No
configDetails = {'invoiceNr': newInvoice, 
				'date' : start_date.strftime('%Y-%m-%d'), 
				'dueDate': end_date.strftime('%Y-%m-%d'),
				'item': item,
				'qty': qty,
				'rate': rate,
				'amount': "{0:.2f}".format(qty * rate),
				'subtotal': str("{0:.2f}".format(qty * rate)) + '\n',
				'total': "{0:.2f}".format(qty * rate),
				'bDue' : "{0:.2f}".format(qty * rate)
				 }


details = [['exampleCSV/clientsExample.csv', 'cleintNickName', clientNickname],
		   ['exampleCSV/mydataExample.csv', 'myNickName', myNickName],
		   ['exampleCSV/bankContactsExample.csv', 'nickname', myNickName],
		   ['exampleCSV/myEmailDataExample.csv', 'emailNickame', myNickName]]


print('about to get all the info')
# append misc Details
for key, value in configDetails.iteritems():
	appendReq(key, value)


# get clientDetails and select by nickname
for i in details:
	getTheInfo(i[0], i[1], i[2])


print('about to initiate connection to google')


creds = SAC.from_json_keyfile_name('client_secret.json',
                                   scopes=["https://www.googleapis.com/auth/drive",
                                           "https://www.googleapis.com/auth/presentations"])


# initialize google slides and Drive API connection
http = creds.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)
SLIDES = discovery.build('slides', 'v1', http=http)
result = service.files().list().execute()
file_list = result["files"]


while "nextPageToken" in result:
    result = self.get_service().files().list(pageToken=result["nextPageToken"]).execute()
    file_list = file_list + result["files"]


for i in file_list:
    if i['name'] == "billingTemplate":
        print('found the template')
        file_id = i['id']


DATA = {'name': 'Invoice ' + str(newInvoice) }
DECK_ID = service.files().copy(body=DATA, fileId=file_id).execute().get('id')
SLIDES.presentations().batchUpdate(body={'requests': reqs},
                                   presentationId=DECK_ID).execute()


data = service.files().export(fileId=DECK_ID,
                              mimeType='application/pdf').execute()
f = open("invoices/"+year+"/"+month+"/"+str(newInvoice)+".pdf", 'wb')
f.write(data)
f.close()

# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

# Define these once; use them twice!


# Create the root message and fill in the from, to, and subject headers

msgRoot = MIMEMultipart('mixed')

subject = varsDict['myName']+" Invoice: #"+str(newInvoice)
msgRoot['Subject'] = subject
msgRoot['From'] = varsDict['myEmail']
msgRoot['To'] = varsDict['clientEmail']
msgRoot.preamble = 'This is a multi-part message in MIME format.'
fp = open("invoices/"+year+"/"+month+"/"+str(newInvoice)+".pdf", 'rb')

attach = MIMEApplication(fp.read(), 'pdf')
fp.close()
attach.add_header('Content-Disposition', 'attachment', filename = 'Invoice_'+str(newInvoice)+'.pdf')
msgRoot.attach(attach)


# We reference the image in the IMG SRC attribute by the ID we give it below
f=codecs.open("emailTemplates/" + varsDict['preferredTemplate'] +'.html' , 'r')

msgText = MIMEText(f.read().replace('{{client}}', varsDict['clientName']), 'html')
msgRoot.attach(msgText)

# This example assumes the image is in the current directory
for filename in glob.glob('emailTemplates/images/'+varsDict['preferredTemplate']+'/*'):
	filesNames = filename.split('/')
	contentID = filesNames[-1].split('.')
	attachEmailImages(filename, contentID[0])

# Send the email (this example assumes SMTP authentication is required)
# print(varsDict)
smtp = smtplib.SMTP(varsDict['host'], varsDict['port'])
smtp.starttls()
smtp.login(varsDict['username'], varsDict['password'])
smtp.sendmail(varsDict['myEmail'], varsDict['clientEmail'], msgRoot.as_string())
smtp.quit()

# save the new invoice number to list of invoices
invoiceDF.to_csv('exampleCSV/invoiceNOExample.csv', index=False)

print('finished')