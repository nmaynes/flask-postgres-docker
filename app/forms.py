from werkzeug.urls import url_encode
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class EditStatusForm(FlaskForm):
    status_text = StringField('Status Update', validators=[DataRequired()])
    published = StringField('Publish On', validators=[DataRequired()])
    submit = SubmitField('Save')

class AddStatusForm(FlaskForm):
    status_text = StringField('Status Update', validators=[DataRequired()])
    published = StringField('Publish On', validators=[DataRequired()])
    submit = SubmitField('Save')