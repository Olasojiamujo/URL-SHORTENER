from .urlshort import db

class URL(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    user_url = db.Column(db.String(255), nullable=True)
    file_content = db.Column(db.LargeBinary, nullable=True)
    filename = db.Column(db.String(255), nullable=True)

    def __init__(self, code, user_url=None, file_content=None, filename=None):
        self.code = code
        self.user_url = user_url
        self.file_content = file_content
        self.filename = filename
