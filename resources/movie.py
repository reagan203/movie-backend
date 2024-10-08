from models import db, MovieModel
from resources.review import review_fields
from flask_restful import Resource, reqparse, marshal_with, fields

# Define movie fields for marshalling response
movie_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "genre": fields.String,
    "description": fields.String,
    "image_url": fields.String,
    "reviews": fields.List(fields.Nested(review_fields))  # Assuming review_fields is already defined
}

class Movie(Resource):
    # Request parser for movie creation and updating
    movie_parser = reqparse.RequestParser()
    movie_parser.add_argument("title", required=True, type=str, help="Enter the movie title")
    movie_parser.add_argument("genre", required=True, type=str, help="Enter the movie genre")
    movie_parser.add_argument("description", type=str, help="Enter the movie description")
    movie_parser.add_argument("image_url", type=str, help="Enter the movie image URL")

    # GET method (Read)
    @marshal_with(movie_fields)
    def get(self, id=None):
        if id:  # Fetch a single movie by ID
            movie = MovieModel.query.filter_by(id=id).first()
            if not movie:
                return {"message": "Movie not found"}, 404
            return movie
        else:  # Fetch all movies
            movies = MovieModel.query.all()
            return movies

    # POST method (Create)
    @marshal_with(movie_fields)
    def post(self):
        args = self.movie_parser.parse_args()
        movie = MovieModel(
            title=args['title'],
            genre=args['genre'],
            description=args.get('description'),
            image_url=args.get('image_url')
        )
        try:
            db.session.add(movie)
            db.session.commit()
            return movie, 201  # Return the created movie and 201 Created status
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating movie: " + str(e)}, 500

    # PUT method (Update)
    @marshal_with(movie_fields)
    def put(self, id):
        movie = MovieModel.query.filter_by(id=id).first()
        if not movie:
            return {"message": "Movie not found"}, 404

        args = self.movie_parser.parse_args()
        movie.title = args['title']
        movie.genre = args['genre']
        movie.description = args.get('description')
        movie.image_url = args.get('image_url')

        try:
            db.session.commit()
            return movie, 200  # Return updated movie
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating movie: " + str(e)}, 500

    # DELETE method (Delete)
    def delete(self, id):
        movie = MovieModel.query.filter_by(id=id).first()
        if not movie:
            return {"message": "Movie not found"}, 404

        try:
            db.session.delete(movie)
            db.session.commit()
            return {"message": "Movie deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting movie: " + str(e)}, 500
