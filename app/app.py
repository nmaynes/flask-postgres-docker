# imports
import os
from flask import Flask
import logging
from config import Config
from flask import Flask, request, render_template, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import db_session
from forms import EditStatusForm
from models import Status


app = Flask(__name__)
app.config.from_object(Config)


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

@app.route('/editStatus/<status_id>', methods=["GET", "POST"])
def edit_status(status_id):

    status = Status.query.filter_by(id=status_id).first_or_404()
    form = EditStatusForm(obj=status)
    if request.method == 'POST' and form.validate():
        status.status_text = form.status_text.data
        status.published = form.published.data
        db.session.commit()
        flash(f'Status {status_id} Updated')

    return render_template('edit_status.html', status=status, form=form)

@app.route('/addStatus/')
def add_status():
    form = EditStatusForm(request.POST)
    if request.method == 'POST' and form.validate():
        status = Status()
        status.status_text = form.status.data
        status.published = form.published.data
        status.save()
        redirect('add_status')
    return render_template('add_status.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
