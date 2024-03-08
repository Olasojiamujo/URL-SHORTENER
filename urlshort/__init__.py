from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__) #name of the modeule running the Flask
    app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'

    db = SQLAlchemy(app)

    # Initialize the database with your Flask app
    db.init_app(app)
    
    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
