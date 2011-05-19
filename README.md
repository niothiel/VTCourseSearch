VT Course Search is my attempt at doing something the current system is lacking. Away to cheat the system if you will. It's a webapp written in python designed to be used only during the DROP/ADD portion of the school year at Virginia Tech.

Currently the way DROP/ADD works for courses when you are enrolled at Virginia Tech is on a first come, first serve basis. Meaning you have to camp drop/add if you ever hope to get a course that you want to take for a semester.

So I thought, why not automate it? I'm a CS major, and I can improve upon their system. I am drawing on my knowledge from my Systems and Networking course to help automate the system.

## Technical Details #################
The entire system is written in Python using the Web.py module. I use Beautiful Soap for parsing the "Classes Timetable" portion of Virginia Tech's website. Beautiful Soap allows full DOM integration, even if the HTML tags are malformed (which they are on this site). There is currently a very *basic* authentication system in place for user accounts, and database support is being built up as I continue working on the project. The backend runs a MySQL server with a very basic schema in place for tracking the submitted requests.

The back-end is a separate python script that connects to the database at specified intervals and uses a script to check whether or not a course is available. If it is, a notification is sent out to the user notifying them of this occurence. After course availability, records will be pruned 3 days after submission, meaning if you miss a slot you will have to resubmit your request if it's been more than three days.

## Installation ###############
First things first, pull the repo from github through the usual means.

Next, since MySQLdb is being used, for the package to work correctly, one must install tow things (On Ubuntu):

	sudo apt-get install libmysqlclient15-dev python-dev

Next install the dependencies using easy\_install, the required dependencies are located in dependencies.txt in the root folder.

After this is done, the basic databases for mysql have to be created. The general syntax for running .sql scripts is the following:

	mysql -u [username] -p [pass] < [script-name-here].sql


Helpful tip:
To save yourself a heartache, you can create a file named .my.cnf on the mysql box (can be the same as the web server box) in the home directory of the current user (~/.my.cnf) with the following text in it:

	[client]
	user="root"
	pass="[ROOT PASSWORD HERE]"

Then changing the permisssions of this file to 700. This allows for a passwordless login to the mysql instance, good for debugging but be mindful of security risks.
