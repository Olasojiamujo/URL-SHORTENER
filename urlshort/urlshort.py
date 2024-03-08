from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bp = Blueprint('urlshort',__name__)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    url = db.Column(db.String(255))
    filepath = db.Column(db.String(255))

    def __init__(self, code, url=None, filepath=None):
        self.code = code
        self.url = url
        self.filepath = filepath

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
            f = request.files['file']
            full_name = code + secure_filename(f.filename)
            f.save('./static/user_files/' + full_name)
            new_url = URL(code=code, filepath=full_name)

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
            return redirect(url_for('static', filename='user_files/' + url_record.filepath))
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
