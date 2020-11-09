I DOnt Think We hAve a NaME

-An explanation of the organization and name scheme for the workspace

Dan's Bagels - 
Luke Barton
Jacob Pope
Braeden Stewart
Jonas Williams-Gilchrist

-Version-control procedures

Each team member has access to all documentation uploaded to Github.
Each team member has instructions for which documentation they should change, as decided in meetings, held at least weekly after class (Mondays, Wednesdays, Fridays after 1:30) or as needed.
Unchanged documents are also available on Github.

-Tool stack description and setup procedure

The project will be done using python and django. Any IDE may be used. Team members will upload their assigned portion of code to the Github repository.

-Build instructions
To run the project, navigate the command line to bagelSite/bagelSite.
Run the commands:

$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py runserver

The site should be hosted at http://localhost:8000/BagelTest/

Build instructions for the main project will be determined in the future

-Unit testing instructions

The unit testing will be done to test each individual method for bugs.
Tests must:
place orders,
manage orders,
manage funds, 
view orders,
change order status,
manage inventory.

-System testing instructions

For best results, the system testing will be done by a human user. This user will go through the methods listed in unit testing in any order, to test each funtion as well as ensuring that the system will not crash in the interim.

-Other development notes, as needed

All file names will be written in lower-camelcase.
