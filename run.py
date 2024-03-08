from urlshort import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()

db = SQLAlchemy(app)

# Initialize the database with your Flask app
db.init_app(app)
