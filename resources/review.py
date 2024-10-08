from models import db, ReviewModel, UserModel, MovieModel
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_jwt_extended import get_jwt_identity, jwt_required

# Define review fields for marshalling response
review_fields = {
    "id": fields.Integer,
    "content": fields.String,
    "rating": fields.Float,
    "user_id": fields.Integer,
    "movie_id": fields.Integer,
    "user": fields.Nested({
        "id": fields.Integer,
        "username": fields.String,
        "email": fields.String,
        "phone": fields.String
    }),
    "movie": fields.Nested({
        "id": fields.Integer,
        "title": fields.String,
        "genre": fields.String,
        "description": fields.String,
        "image_url": fields.String
    })
}

class Review(Resource):
    # Request parser for review creation and updating
    review_parser = reqparse.RequestParser()
    review_parser.add_argument("content", required=True, type=str, help="Enter the review content")
    review_parser.add_argument("rating", required=True, type=float, help="Enter the review rating")

    # GET method (Read)
    @marshal_with(review_fields)
    def get(self, id=None):
        if id:  # Fetch a single review by ID
            review = ReviewModel.query.filter_by(id=id).first()
            if not review:
                return {"message": "Review not found"}, 404
            return review
        else:  # Fetch all reviews
            reviews = ReviewModel.query.all()
            return reviews

    # POST method (Create) - Here, we extract user_id from JWT and movie_id from the URL
    @jwt_required()
    @marshal_with(review_fields)
    def post(self, movie_id):
        args = self.review_parser.parse_args()

        # Extract user_id from JWT (requires that the user is logged in)
        user_id = get_jwt_identity()
        
        # Check if the movie exists
        movie = MovieModel.query.filter_by(id=movie_id).first()
        if not movie:
            return {"message": "Movie not found"}, 404

        review = ReviewModel(
            content=args['content'],
            rating=args['rating'],
            user_id=user_id,
            movie_id=movie_id
        )

        try:
            db.session.add(review)
            db.session.commit()
            return review, 201  # Return the created review and 201 Created status
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating review: " + str(e)}, 500

    # PUT method (Update) - Here, no need for movie_id or user_id since it's an update
    @jwt_required()
    @marshal_with(review_fields)
    def put(self, id):
        review = ReviewModel.query.filter_by(id=id).first()
        if not review:
            return {"message": "Review not found"}, 404

        args = self.review_parser.parse_args()
        review.content = args['content']
        review.rating = args['rating']

        try:
            db.session.commit()
            return review, 200  # Return updated review
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating review: " + str(e)}, 500

    # DELETE method (Delete)
    @jwt_required()
    def delete(self, id):
        review = ReviewModel.query.filter_by(id=id).first()
        if not review:
            return {"message": "Review not found"}, 404

        try:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting review: " + str(e)}, 500
