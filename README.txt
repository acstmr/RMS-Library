LIBRAIN - Library Management System
MEMBERS:  Chris Angelo Rollon
          Armand Christian N. Sta. Maria

A modern library management system built with Python Flask and MySQL.

===============================

HOW TO SET UP LIBRAIN

Open the downloaded LIBRAIN folder on your computer.

Open a terminal window inside the folder.

Change directory:
Type the following one by one in the terminal:
cd LIBRAIN-main
cd LIBRAIN

Create a virtual environment:
Type in the terminal:
python -m venv venv

Why use a virtual environment?
A virtual environment is used to keep your project's dependencies isolated. This means the packages you install for this project will not affect other Python projects on your computer. It helps avoid version conflicts and keeps your system clean.

Select the Python interpreter:
In your code editor (for example, VS Code), open the command palette using Ctrl+Shift+P
Search for "Python: Select Interpreter"
Click "Enter interpreter path"
Paste the path:
venv/scripts/python

Install the required packages:
Type the following in the terminal:
pip install flask
pip install mysql-connector-python

Open the XAMPP Control Panel.
Start both Apache and MySQL services.

Open your web browser and type:
localhost

Click on phpMyAdmin.

Create a new database named:
library_db

Import the database:
Click the Import tab and upload the file named schema.sql from the "database" folder.
You can also import sample_data.sql if you want to include sample records.

Run the application:
In the terminal, type:
python login_backend.py

After running the server, a link will appear in the terminal.
Open the link in your browser:
http://localhost:5000

===============================

DEFAULT LOGIN CREDENTIALS

Librarian
Username: mama
Password: 1111

Admin
Username: kaito
Password: 1111

===============================

TROUBLESHOOTING
If the database is not connecting:
- Make sure MySQL is running in XAMPP
- Check the database credentials in your .env file
- Confirm the library_db database and its tables exist in phpMyAdmin
If packages are missing or not working:
- Check installed packages using pip list
- Reinstall by typing: pip install -r requirements.txt --force-reinstall
If port 5000 is already in use:
- Open the login_backend.py file
- Change the port number to something else like 5001

===============================

NEED HELP?
Review the Troubleshooting section
Check for error messages in the terminal
Contact your system administrator for support

