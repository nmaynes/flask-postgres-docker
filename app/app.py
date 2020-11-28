# imports
import os
from flask import Flask
import logging
import config as cfg
from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from forms import EditStatusForm
from models import Status


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['DBNAME']
)

db = SQLAlchemy(app)
MIGRATE = Migrate(app, db)

logging.getLogger().setLevel(logging.INFO)




@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    statuses = Status.query.all()
    return render_template('index.html', data=statuses)

@app.route('/status/<status_id>')
def show_user(status_id):
    status = Status.query.filter_by(id=status_id).first_or_404()
    return render_template('show_status.html', status=status)

@app.route('/editStatus/<status_id>')
def edit_status(status_id):
    form = EditStatusForm()
    status = Status.query.filter_by(id=status_id).first_or_404()
    return render_template('edit_status.html', status=status, form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
