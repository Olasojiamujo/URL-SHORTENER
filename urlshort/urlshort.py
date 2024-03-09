from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
from sqlalchemy import Column, Integer, String, Float
from werkzeug.utils import secure_filename
from .__init__ import db

bp = Blueprint('urlshort', __name__)

class URL(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    file_content = db.Column(db.LargeBinary, nullable=True)  # Store file content
    filename = db.Column(db.String(255), nullable=True)  # Store original filename

    def __init__(self, code, url=None, file_content=None, filename=None):
        self.code = code
        self.url = url
        self.file_content = file_content
        self.filename = filename

#creating a route
@bp.route('/') #redirect to the base url.
def home(): #this is a regular python code
    return render_template('home.html', codes=session.keys())
#    return render_template('home.html', name='Ola')

@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        code = request.form['code']
        existing_url = URL.query.filter_by(code=code).first()

        if existing_url:
            flash('That Shortname has already been taken. Please use another short name')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            new_url = URL(code=code, url=request.form['url'])
        else:
            file = request.files['file']
            file_content = file.read()
            new_url = URL(code=code, file_content=file_content, filename=secure_filename(file.filename))

        db.session.add(new_url)
        db.session.commit()
        session[code] = True
        return render_template('your_url.html', code=code)
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    url_record = URL.query.filter_by(code=code).first()
    if url_record:
        if url_record.url:
            return redirect(url_record.url)
        else:
            # Handling file serving is more complex. Consider uploading to a service like S3 and serving from there.
            abort(404)  # Simplified for this example
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
