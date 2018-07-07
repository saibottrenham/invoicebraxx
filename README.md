# invoicebraxx
Nifty little invoicing tool to speed up my Sole trader invoicing process

## Set up instructions

install requirements with 

	pip install -r req.txt

Google Slides API instructions
https://developers.google.com/slides/quickstart/python

NOTE:
Use a service account so that you don't have to go through the click authentication process. 

create your own Invoice template with Google Slides inside your personal google drive and 
use the service account email to give access to the service account.

check the PDF as an example.

For the Emailing process I used https://beefree.io/templates/
to create a Basic html thank you Email with links to my Linkedin

inorder to get the images appear in your email, you have to replace the /images/...png urls with 
cid:Content-IDs

eg:

	/images/clouds_outline.png
	
becomes:

	cid:clouds_outlines

## Config
The ongoing invoice number can be set inside invoiceNOExample.csv
the increment rate can be edited on line 71 inside invoiceYou.py

The Date is set for the day of invoice generation.
The Due Date is creation date plus 7 days.

It can be changed on line 55 inside invoiceYou.py

Bank contacts are stored inside 
bankContactsExample.csv

Clients are stored inside clientsExample.csv and can be selected via client nickname 

The same schema for personal data which is inside mydataExample.csv

Remember to enable your SMTP service if you want it to use with email functionality

Note:
if you want to proof read your Invoice before sending them out to a client, you can easily sent them 
to yourself and then forward them until a preview functionality is not setup


## how to run

	python invoiceYou.py

The Script will ask you several questions e.g.

	Select from the options below:

	profile1
	profile2
	profile3
	...

	Please Select Your NickName: profile1
	Select from the options below:

	client1
	client2
	client3
	...

	What is your Rate? Please only Numbers: 240
	What is your QTY? Please only Numbers: 10
	What kind of Work?: Webdevelopment and Consulting
	Add Another Item? press enter to continue. To exit type no : 
	What is your Rate? Please only Numbers: 100
	What is your QTY? Please only Numbers: 1
	What kind of Work?: New Website Template
	Add Another Item? press enter to continue. To exit type no : no
	about to get all the info
	about to initiate connection to google
	found the template
	PDF Generation Finished, next up Sending the Email
	finished

## update log

### 07.07.2018

- added light version of multiline input. Changed the template slightly for that functionality to happen.
- In order for that to work I created a few more input prompts that ask for all the line items one by one.
- maybe needs some improvement in terms of input efficency in the future. Probably when setting up a web 
- Frontend

### 26.06.2018

 - added input prompt so that user's dont have to recall their clients and nicknames from memory

### 10.06.2018

 - initial commit


## todo and next steps

further development includes

* preview functionality
* code execution via voice command
* multi page invoices if more then 10 line items
* set up tax options
* cleaning up, refactoring this big monolithic clusterf***
* implementing inside a webapplication, possibly django
* connect to an accounting system
