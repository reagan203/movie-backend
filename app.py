import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from models import db, UserModel
from resources.user import User
from resources.movie import Movie
from resources.review import Review

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Allow CORS only for frontend's origin
CORS(app, origins=["http://localhost:3000"])

# Initialize extensions
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Database and JWT configuration from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
migrations = Migrate(app, db)

# Get the current user from JWT
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = UserModel.query.filter_by(id=identity).one_or_none()
    return user.to_json() if user else None

# Login Route (Simplified without Flask-RESTful)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = UserModel.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# User Registration, Movies, and Reviews Resources
api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Movie, '/movies', '/movies/<int:id>')
api.add_resource(Review, '/movies/<int:movie_id>/reviews', '/reviews/<int:id>')

# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
