#this is the models.py that is going to hold all the different tables required for this project
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import check_password_hash

# initialize the SQLAlchemy object
db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(130),nullable=False)
    
    def check_password(self, password):
        return check_password_hash(self.password , password)
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone':self.phone
        }

class MovieModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True) 
    reviews = db.relationship('ReviewModel', backref='movie', lazy=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'description': self.description,
            'image_url': self.image_url,  
        }


class ReviewModel(db.Model):
    __tablename__ ='reviews'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel', backref='reviews',lazy=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'user': self.user.to_json() if self.user else None,
            'movie': self.movie.to_json() if self.movie else None
        }
    