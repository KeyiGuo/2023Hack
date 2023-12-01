import json
from db import db, Library, Posts
from flask import Flask, request
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
db_filename = "studybuddy.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)


db.init_app(app)
with app.app_context():
    db.create_all()
    library_names = ["Uris Library", "Olin Library", "Mann Library"]
    for name in library_names:
        library = Library(library_name=name)
        db.session.add(library)
    db.session.commit()


def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/")
@app.route("/api/posts/")
def get_all_posts():
    """
    Endpoint for getting all posts
    """
    return_posts = [posts.serialize() for posts in Posts.query.all()]
    return success_response(return_posts)


@app.route("/api/posts/<int:library_id>/", methods=["POST"])
def create_post(library_id):
    """
    Endpoint for creating a new post
    """

    body = json.loads(request.data)
    message = body.get("message")
    
    if message is None:
        return failure_response("message", 400)
    
    library = Library.query.filter_by(id = library_id).first()
    if library is None:
        return failure_response("Library not found!")

    newPost = Posts(
        time=datetime.now(),
        message=message,
        library_id=library_id
)
    db.session.add(newPost)
    db.session.commit()

    return success_response(newPost.serialize(), 201)


@app.route("/api/posts/<int:library_id>/")
def get_posts_from_library(library_id):
    """
    Endpoint for getting posts of a certain library
    """

    library = Library.query.filter_by(id = library_id).first()
    if library is None:
        return failure_response("Library not found!")
    
    return success_response(library.serialize())


@app.route("/api/posts/<int:id>/", methods=["DELETE"])
def delete_post(id):
    """
    Endpoint for deleting a post by post_id
    """
    post = Posts.query.filter_by(post_id = id).first()
    if post is None:
        return failure_response("post not found")
    serialized_post = post.serialize()
    db.session.delete(post)
    db.session.commit()
    return success_response(serialized_post)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8000,debug = True)
