from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
from werkzeug.utils import secure_filename
from .extensions import db
from .routes import main
import os

bp = Blueprint('urlshort',__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.environs.get("DATABASE_URL")

#replaced by Blueprint
#app = Flask(__name__) #name of the modeule running the Flask
#app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'

#print(__name__)

#creating a route
@bp.route('/') #redirect to the base url.
def home(): #this is a regular python code
    return render_template('home.html', codes=session.keys())
#    return render_template('home.html', name='Ola')

@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls ={}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That Shortname already been taken. Please use another short name')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('./static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}


        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
        #return render_template('your_url.html', code=request.args['code']) change to form when working with post request
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
