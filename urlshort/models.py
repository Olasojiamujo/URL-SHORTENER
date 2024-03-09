from .extensions import db

class SHORTNAME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    file_content = db.Column(db.LargeBinary, nullable=True)
    filename = db.Column(db.String(255), nullable=True)

    def __init__(self, code, url=None, file_content=None, filename=None):
        self.code = code
        self.url = url
        self.file_content = file_content
        self.filename = filename
