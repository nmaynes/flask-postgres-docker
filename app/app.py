# imports
import os
from flask import Flask
import logging
import appconfig as cfg
from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from routes.mainmenu_rt import mainmenu_rt


app = Flask(__name__)

app.register_blueprint(mainmenu_rt)


# this is a very useful setting for automatically reloading html changes
# https://stackoverflow.com/questions/9508667/reload-flask-app-when-template-file-changes

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['DBNAME']
)

db = SQLAlchemy(app)
MIGRATE = Migrate(app, db)

logging.getLogger().setLevel(logging.INFO)


class Friend(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthday_id = db.Column(db.Integer, db.ForeignKey('birthdays.id'), nullable=False)
    birthday = db.relationship("Birthday", backref=db.backref('friend', lazy=True))

    def __repr__(self):
        return '<Birthday %r>' % self.name

class Birthday(db.Model):
    __tablename__ = 'birthdays'
    id = db.Column(db.Integer, primary_key=True)
    birthdate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Birthday %r>' % self.birthdate

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/birthdays')
def view_birthdays():
    birthdays = Birthday.query.all()
    return render_template('birthdays.html', data=birthdays)

if __name__ == '__main__':
    app.run(host=cfg.appcfg['host'], debug=cfg.appcfg['debug'])
