from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create the SQLAlchemy db instance globally
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__) # Name of the module running the Flask app

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # Example for SQLite, adjust for your DB
    app.secret_key = 'your_secret_key'  # Set a secret key for sessions and cookies

    # Initialize the database with your Flask app
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create database tables for our data models

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
