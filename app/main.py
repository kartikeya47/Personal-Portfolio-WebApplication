from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime

db_uri = os.environ.get('DB_URI', None)

app = Flask(__name__)

s_key = os.environ.get('SECRET_KEY', None)

app.secret_key = s_key

with open('app/templates/config.json', 'r') as c:
    params = json.load(c)["params"]

db = SQLAlchemy(app)

if params['local_server'] == True:
    pass
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(40), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Blogs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    blog_link = db.Column(db.String(120), nullable=False)
    writer_name = db.Column(db.String(120), nullable=False)
    slug_name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)



@app.route("/")
def index():
    blogs = Blogs.query.all()
    return render_template('index.html', params=params, blogs=blogs)


@app.route("/blog/<string:slug>")
def blog_page(slug):
    blog1 = Blogs.query.filter_by(slug_name=slug).first()
    return render_template("blog.html", blog1=blog1, params=params)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        contacts = Contacts(name=name, email=email, subject=subject, message=message, date=datetime.now())
        db.session.add(contacts)
        db.session.commit()
        return redirect("/")
    return render_template("index.html", params=params)