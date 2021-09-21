# FinancePeer

Step 1> Create a virtual environment as follows:
	-> Go to folder where you've downloaded the files
	-> open a cmd in that directory
	-> Type following command ```py -3 -m venv venv```
	-> After the venv has been created, type the following ```venv\Scripts\activate``` to activate the virtual environment
	-> I have provided the requirements.txt, install it using the following command ```pip install -r requirements.txt```
<br />
Step 2> Download and install xampp from here : https://www.apachefriends.org/index.html
<br />
Step 3> Open the xampp control panel and start the Apache Server and MySQL Database.
<br />
Step 4> Click on the admin tab (in MySQL)of xampp control panel which will open phpmyadmin.
<br />
Step 5> After you are in phpmyadmin, create a new database named "finpeer'
<br />
Step 6> After the db has been created, click on finpeer and go to import tab at the top of the page.
<br />
Step 7> Now under "File to import" Choose the database.sql file which I have provided and click "GO" on the bottom of the page.
<br />
Step 8> Now open the cmd and activate the virtual environment using ```venv\Scripts\activate``` incase it is not activated and type ```py main.py``` to start the flask app.
<br />
Step 9> Copy the url which is flashing in the cmd to open the app in your local machine.
<br />