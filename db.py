from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Posts(db.Model):
    """
    Posts Model
    """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    subject = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable = False)

    def serialize(self):
        """
        serialize posts information
        """
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "subject": self.subject,
            "content": self.content,
            "user_id" : self.user_id
        }
    
class Users(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    major=  db.Column(db.String, nullable=False)
    year_of_school = db.Column(db.String, nullable=False)
    profile_photo = db.Column(db.String, nullable=False)
    intro = db.Column(db.String, nullable=False)
   
    posts = db.relationship('Posts', cascade = "delete")

    def serialize(self):
        """
        serialize user information
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "major": self.major,
            "year of school": self.year_of_school,
            "profile photo": self.profile_photo,
            "self introduction": self.intro,
            "posts": [post.serialize() for post in self.posts]
            }  
