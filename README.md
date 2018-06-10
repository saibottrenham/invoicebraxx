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

	python invoiceYou.py myNickName cleintNickName  rate qty item

Example:

	python invoiceMe.py 'toby' 'mrOne' 150 10 'Webdevelopment and consulting'


## todo and next steps

further development includes

* preview functionality
* input prompting maybe
* create multi line Item functionality (multi page invoices)
* set up tax options
* cleaning up, refactoring this big monolithic clusterf***
* implementing inside a webapplication, possibly django
* connect to an accounting system
