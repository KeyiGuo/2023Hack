from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Posts(db.Model):
    """
    Posts Model
    """
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(), nullable=False)
    message = db.Column(db.String, nullable=False)
    library_id = db.Column(db.Integer, db.ForeignKey("library.id"), nullable=False)


    library = db.relationship('Library', backref=db.backref('posts', cascade="delete"))

    def serialize(self):
        """
        Serialize posts information
        """
        return {
            "id": self.post_id,
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": self.message,
            "library": self.library.library_name
        }

class Library(db.Model):
    """
    Library model
    """
    __tablename__ = "library"
    id = db.Column(db.Integer, primary_key=True)
    library_name = db.Column(db.String, nullable=False)


    def serialize(self):
        """
        Serialize posts information
        """
        return [p.serialize() for p in self.posts]


