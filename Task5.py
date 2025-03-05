from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Stores hashed password

# Helper Functions
def is_valid_email(email):
    """Validate email format."""
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

def is_strong_password(password):
    """Ensure password has at least 8 chars, 1 digit, and 1 uppercase letter."""
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isupper() for c in password)

# Signup API
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate email format
        if not is_valid_email(email):
            return {'message': 'Invalid email format'}, 400
        
        # Validate password strength
        if not is_strong_password(password):
            return {'message': 'Password must be at least 8 characters long, contain a number, and an uppercase letter'}, 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400
        
        # Hash password before storing
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User registered successfully'}, 201

# Login API
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 401
        
        return {'message': 'Login successful'}, 200

# View All Users API (Excludes Passwords)
class GetUsers(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email,'passsword':user.password} for user in users]
        return jsonify(user_list)

# Register API Endpoints
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(GetUsers, '/users')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
