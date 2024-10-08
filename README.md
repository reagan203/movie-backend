Movie Review App (Backend)
This is a backend Flask application for managing movie reviews. It uses Flask-SQLAlchemy as the ORM and Flask-RESTful for creating APIs. The app allows users to perform CRUD operations on movie reviews, manage users, and handle user authentication.

Prerequisites
Make sure you have Python 3.8+ installed on your system.

Steps to Set Up and Run the Application
1. Create a Virtual Environment
To isolate your project dependencies, create a virtual environment:

bash
Copy code
python3 -m venv .venv
2. Activate the Virtual Environment
Activate the virtual environment using:

On macOS/Linux:
bash
Copy code
source .venv/bin/activate
On Windows:
bash
Copy code
.venv\Scripts\activate
3. Install Dependencies
Run the following command to install all the necessary packages and dependencies:

bash
Copy code
pip install -r requirements.txt
4. Database Setup
The app uses Flask-Migrate and SQLAlchemy to manage the database schema. To initialize and configure the database, follow these steps:

Initialize the migration environment:
bash
Copy code
flask db init
Generate a new migration file with schema changes:
bash
Copy code
flask db revision --autogenerate -m "Initial migration"
Apply the migration to your database:
bash
Copy code
flask db upgrade
5. Project Structure
Here's an overview of the project structure:

graphql
Copy code
.
├── app.py               # Main application file
├── models.py            # Holds the SQLAlchemy models
├── resources/           # CRUD logic for user, movies, and reviews
│   ├── movies.py
│   ├── review.py
│   └── user.py
├── migrations/          # Directory for Alembic migrations
├── .env                 # Environment variables (e.g., secret keys, database URL)
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation (this file)
6. Setting Up Environment Variables
Create a .env file to store sensitive data such as database URLs, JWT secret keys, etc. Make sure to add this file to .gitignore to avoid exposing sensitive information.

Example .env file:

makefile
Copy code
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///movies.db
7. Models
The following tables are used in the app, defined in models.py:

User: Stores user details such as username, password, etc.
Movie: Stores information about movies.
Review: Stores movie reviews submitted by users.
8. CRUD Operations
The logic for managing CRUD operations is housed in the resources folder. Each resource handles operations for:

movies.py: Logic for adding, updating, retrieving, and deleting movies.
review.py: Logic for adding, updating, retrieving, and deleting reviews.
user.py: Logic for user registration, authentication, and profile management.
9. Running the Application
To run the application, execute the following command:

bash
Copy code
flask run
The application will start on http://127.0.0.1:5000/.

10. Freezing Dependencies
After adding any new dependencies or updating the project, ensure to update the requirements.txt file:

bash
Copy code
pip freeze > requirements.txt
This will list all installed packages and their versions, ensuring consistency in future setups.

Additional Notes:
Flask-JWT-Extended: Used for handling JWT authentication.
Flask-Migrate: Used for database migrations.
Flask-Bcrypt: Used for hashing user passwords securely.
Flask-CORS: Handles Cross-Origin Resource Sharing to allow interaction with a frontend app.
# movie-backend
