import os

from flask import Flask, render_template
from .extensions import db
from .urlshort import bp


def create_app(test_config=None):
    app = Flask(__name__) # Name of the module running the Flask app

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # Example for SQLite, adjust for your DB
    app.secret_key = 'your_secret_key'  # Set a secret key for sessions and cookies
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @app.cli.command('db_create')
    def db_create():
        db.create_all()
    # Initialize the database with your Flask app
    db.init_app(app)

    app.register_blueprint(bp)

    # Application-wide error handler
    @app.errorhandler(404)
    def page_not_found_appwide(error):
        return render_template('page_not_found.html'), 404

    @app.errorhandler(Exception)
    def handle_exception(error):

        # Log the error for debugging
        app.logger.error(f'Unhandled Exception: {error}')

        return render_template('page_not_found.html'), 500

    return app
