#!/bin/python
from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request, g, session
from flask import render_template_string
from datetime import timedelta
# from flask_github import GitHub
import os
# from werkzeug import secure_filename
import dockers
import aws_filters
from flask_github import GitHub
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'sqlite:////tmp/github-flask.db'
SECRET_KEY = 'development_key'
DEBUG = True

# Set these values
GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']


app = Flask(__name__)
app.config.from_object(__name__)

# setup github-flask
github = GitHub(app)

# setup sqlalchemy
engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    github_access_token = Column(String(200))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        return None
    if 'static' in request.path or 'login' in request.path or 'github-callback' in request.path:
        return None
    return redirect(url_for('login'))    

        
    
@app.after_request
def after_request(response):
    db_session.remove()
    return response

@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return render_template('login.html')        
    else:
        a = github.get('user')
        print(a)
        return str(session['user_name'])

@app.route('/login_github')
def login_github():
    return github.authorize()
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login')) 

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    if access_token is None:
        return redirect("/")

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)
    user.github_access_token = access_token
    db_session.commit()
    session['user_id'] = user.id
    return redirect("/")


@app.context_processor
def inject_user():
    if request.path == "/login":
        return dict(user='')
    return dict(user=github.get('user')['name'])

@app.route('/user')
def user():
    test = github.get('user')['name']
    return str(test)

@app.route('/')
def index():
	return redirect(url_for('docker'))


@app.route('/docker', methods=["POST", "GET"])
def docker(name=None):
    if 'search' in request.args:
        search = request.args['search']
        return render_template('docker.html', dockers=dockers.search_docker(dockers.docker_name_up(), search))
    elif 'intro' in request.args:
        docker_host = request.args['docker_host']
        docker_id = request.args['docker_id']
        return render_template('docker_intro.html', docker=dockers.docker_intro(docker_host, docker_id))
    elif 'docker_log' in request.args:
        docker_host = request.args['docker_host']
        docker_id = request.args['docker_id']
        return render_template('docker_logs.html', dockers=dockers.docker_logs(docker_host, docker_id), docker_id=docker_id, docker_host=docker_host)
    elif 'docker_top' in request.args:
        docker_host = request.args['docker_host']
        docker_id = request.args['docker_id']
        return render_template('docker_top.html', dockers=dockers.docker_top(docker_host, docker_id), docker_id=docker_id, docker_host=docker_host)
    else: 
        return render_template('docker.html', dockers=dockers.docker_name_up(), test=request.args.get('folder'))

@app.route('/aws', methods=["POST", "GET"])
def aws(name=None):
    if 'search' in request.args:
        return render_template('aws.html', instances=aws_filters.aws_instanses_filter(request.args['search']))
    else: 
        return render_template('aws.html', instances=aws_filters.aws_instanses_filter())

init_db()
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=8080, debug=True)










