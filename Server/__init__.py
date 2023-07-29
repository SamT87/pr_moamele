from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)

app.config["SECRET_KEY"] = "c4c921b87279975be63eb5779d6a4d00bf59723f5cedcf16591eb7e250c3f225"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=1)


db = SQLAlchemy(app)
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    user = db.Column(db.String,primary_key=True)
    password = db.Column(db.String)
    admin = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.email}'

# make database
# with app.app_context():
#     db.create_all()


import Server.views
