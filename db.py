import mysql.connector
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()

class Database():
    def __init__(self, creds):
        host = creds["host"]
        user = creds["user"]
        password = creds["password"]
        database = creds["database"]
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        self.cursor = self.conn.cursor()

    def generateId(self, body):
        postId = hashlib.sha1(body.encode("UTF-8")).hexdigest()[:12]
        sql = "SELECT * FROM posts WHERE postId='{0}'".format(postId)
        self.cursor.execute(sql)
        posts = self.cursor.fetchall()
        if len(posts) > 0:
            # In event of hash collision, hashing is performed
            # again recursively until a unique hash is found.
            postId = self.generateId(postId)
        return postId

    def addPost(self, post):
        postId = self.generateId(post.body)
        sql = "INSERT INTO POSTS (postId, title, body, user, tags) VALUES (%s, %s, %s, %s, %s)"
        vals = (postId, post.title, post.body, post.meta["user"], ','.join(post.meta["tags"]))
        self.cursor.execute(sql, vals)
        self.conn.commit()
        return postId
    
    def fetchPost(self, postId):
        sql = f"SELECT * FROM posts WHERE postId='{postId}'"
        self.cursor.execute(sql)
        post = self.cursor.fetchall()
        return post

class Post():
    # Example post:
    # meta = {"user": "clubby789", "tags": ["python", "mysql"]}
    # myDb.addPost(Post("I can't code", "I can't code anything, can anyone help?", meta))
    def __init__(self, title, body, meta):
        self.title = title
        self.body = body
        self.meta = meta


if __name__=='__main__':
    conn = mysql.connector.connect(
        host="localhost",
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        database="stackunderflow"
    )
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS \
posts (postId VARCHAR(12) PRIMARY KEY, title VARCHAR(255), body VARCHAR(3000), \
user VARCHAR(30), tags VARCHAR(2048));\
    """)
    conn.commit()
    