from flask import Flask
import click
from flask.cli import with_appcontext
from .urlshort import db
import os

def create_app(test_config=None):
    app = Flask(__name__) # Name of the module running the Flask app

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # Example for SQLite, adjust for your DB
    app.secret_key = 'your_secret_key'  # Set a secret key for sessions and cookies
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with your Flask app
    db.init_app(app)

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    @click.command(name='create_tables')
    @with_appcontext
    def create_tables():
        db.create_all()

    return app
