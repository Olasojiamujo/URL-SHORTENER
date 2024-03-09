from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint, send_from_directory
import os
from werkzeug.utils import secure_filename
from .models import SHORTNAME
from .extensions import db

bp = Blueprint('urlshort', __name__)

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
        existing_url = SHORTNAME.query.filter_by(code=code).first()

        if existing_url:
            flash('That Shortname has already been taken. Please use another short name')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            new_url = SHORTNAME(code=code, url=request.form['url'])
        else:
            file = request.files['file']
            if file:  # Check if a file is actually uploaded
                file_content = file.read()
                new_url = SHORTNAME(code=code, file_content=file_content, filename=secure_filename(file.filename))
            else:
                flash('No file uploaded.')
                return redirect(url_for('urlshort.home'))

        db.session.add(new_url)
        db.session.commit()
        session[code] = True
        return render_template('your_url.html', code=code)
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    url_record = SHORTNAME.query.filter_by(code=code).first()
    if url_record:
        if url_record.url:
            return redirect(url_record.url)
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
