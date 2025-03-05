## Objective:
Create a simple REST API that allows users to sign up and log in using Flask.

## User Registration (Signup API)
Accepts username, email, password
Hash passwords before storing them in the database
Validate email format and password strength
Prevent duplicate email registrations

## User Login (Login API)
Accepts email and password
Compares the password with the hashed one in the database
Returns a success message 

## Tech Stack for Phase 1
Flask (Flask-RESTful, Flask-SQLAlchemy)
SQLite (For storing user data)
Werkzeug (For password security)
 
