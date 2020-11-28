from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import Base

app = Flask(__name__)
db = SQLAlchemy(app)


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    published = db.Column(db.Date, nullable=True)
    status_text = db.Column(db.UnicodeText, nullable=False)

    def __repr__(self):
        published_on = "Unpublished"
        if self.published:
            published_on = f"Published on {self.published}"
        return f"<Status {self.status_text} - {published_on}>"
