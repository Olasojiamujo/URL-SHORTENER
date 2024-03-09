from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint, send_from_directory
import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from werkzeug.utils import secure_filename

# Create the SQLAlchemy db instance globally
db = SQLAlchemy()

bp = Blueprint('urlshort', __name__)

class URL(db.Model):
    __tablename__ = 'url'  # Changed to 'urls' to avoid potential SQL keyword conflict
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

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(bp.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        code = request.form['code']
        existing_url = URL.query.filter_by(code=code).first()

        if existing_url:
            flash('That Shortname has already been taken. Please use another short name')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            new_url = URL(code=code, user_url=request.form['user_url'])
        else:
            file = request.files['file']
            if file:  # Check if a file is actually uploaded
                file_content = file.read()
                new_url = URL(code=code, file_content=file_content, filename=secure_filename(file.filename))
            else:
                flash('No file uploaded.')
                return redirect(url_for('urlshort.home'))

        db.session.add(new_url)
        db.session.commit()
        return render_template('your_url.html', code=code)
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    url_record = URL.query.filter_by(code=code).first()
    if url_record:
        if url_record.user_url:
            return redirect(url_record.user_url)
        else:
            abort(404)
    else:
        abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
