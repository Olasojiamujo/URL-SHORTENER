import os
from flask import Flask, render_template
from .extensions import db
from .urlshort import bp


def create_app(test_config=None):
    app = Flask(__name__) # Name of the module running the Flask app

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # set the DATABASE_URL in your environment
    app.secret_key = 'your_secret_key'  # Set a secret key for sessions and cookies
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with your Flask app
    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all() #to create your database
        db.session.commit() #always remember to commit

    return app
