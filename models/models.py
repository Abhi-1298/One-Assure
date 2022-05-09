from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from sqlalchemy.orm import relationship,backref
from sqlalchemy import Index
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project_db:1234@localhost:5432/project_db_name"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# User details model
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = password

    # def __repr__(self):
    #     return f"{self.id}"

    # def __str__(self):
    #     return f"{self.id}"

    # def get_user(self, id):
    #     return self

class Session(db.Model):    
    __tablename__ = "session"

    access_token = db.Column(db.String(300), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship(User, uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id


# File Upload(One to Many:Relationship)

class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    columns = relationship("Column", backref=backref("files", cascade="all,delete"))

class Column(db.Model):
    __tablename__ = "columns"

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer,ForeignKey('files.id'))
    col_name = db.Column(db.String(200))
    row_pos = db.Column(db.Integer)
    col_row_data = db.Column(db.Text)

    Index('file_id_col_row_idx', file_id, col_name, row_pos)
    



# db.session.add(User)
db.create_all()

