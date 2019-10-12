from flask import Flask, render_template, request, redirect
import os
import atexit
from dotenv import load_dotenv
from db import Database, Post
import time

basedir = os.path.abspath(os.path.dirname(__file__))

def handleExit():
    os.system('mysql.server stop')
atexit.register(handleExit)
envPath = os.path.join(basedir, '.env')
load_dotenv(envPath)

creds = {
    "host":"localhost",
    "user":os.environ['DB_USER'],
    "password":os.environ['DB_PASS'],
    "database":"stackunderflow"
}

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def index(user=None):
    return render_template('index.html')

@app.route('/submit', methods=["POST"])
def submitPost():
    meta = {"tags":request.form.get("tags").split(','), "user":"clubby789"}
    post = Post(request.form.get("title"), request.form.get("body"), meta)
    postId = db.addPost(post)
    return redirect(f"/post/{postId}", code=302)

@app.route('/post/<postId>')
def viewPost(postId):
    post = db.fetchPost(postId)[0]
    postDict = {"title": post[1], "body": post[2], "user": post[3], "tags": post[4]}
    return render_template('post.html', postTitle = postDict["title"], postBody = postDict["body"])

if __name__ == '__main__':
    
    os.system('mysql.server start')
    time.sleep(5)
    db = Database(creds)
    app.run(debug=True)