from flask import Flask
from .commands import create_tables
from .urlshort import db
from .urlshort.bp import bp
import os

def create_app(test_config=None):
    app = Flask(__name__) # Name of the module running the Flask app

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # Example for SQLite, adjust for your DB
    app.secret_key = 'your_secret_key'  # Set a secret key for sessions and cookies
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with your Flask app
    db.init_app(app)

    app.register_blueprint(bp)

    app.cli.add_command(create_tables)

    return app
