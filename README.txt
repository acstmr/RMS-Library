LIBRAIN - Library Management System
MEMBERS: Chris Angelo Rollon
	 Armand Christian N Sta. Maria
===============================

A modern library management system built with Python Flask and MySQL.

System Requirements
-----------------
1. Python 3.8 or higher
2. MySQL 8.0 or higher
3. Web browser (Chrome, Firefox, or Edge recommended)

Required Python Packages
----------------------
- Flask
- mysql-connector-python
- python-dotenv
- Werkzeug

Setup Instructions
----------------

1. Database Setup:
   - Install MySQL if not already installed
   - Create a new database named 'library_db'
   - Import the database schema from 'database/schema.sql'
   - Import sample data from 'database/sample_data.sql' (optional)

2. Python Environment:
   - Install Flask
     ```
     pip install flask
     ```
   - Install required packages:
     ```
     pip install -r requirements.txt
     ```
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
       ```
       venv\Scripts\activate.bat
       ```
   

Running the Application
---------------------
1. Make sure your MySQL server is running
2. Activate the virtual environment (if not already activated)
3. Run the application:
   ```
   python login_backend.py
   ```
4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

Default Login Credentials
-----------------------
Librarian:
- Username: mama
- Password: 1111

Admin:
- Username: kaito
- Password: 1111


Troubleshooting
--------------
1. Database Connection Issues:
   - Verify MySQL is running
   - Check database credentials in .env file
   - Ensure database and tables exist

2. Package Issues:
   - Verify all packages are installed:
     ```
     pip list
     ```
   - Try reinstalling requirements:
     ```
     pip install -r requirements.txt --force-reinstall
     ```

3. Port Conflicts:
   - If port 5000 is in use, modify the port in app.py
   - Check if another application is using the same port

Support
-------
For issues and support:
1. Check the troubleshooting section
2. Review error logs in 'logs' directory
3. Contact system administrator
