from flask_wtf import FlaskForm
import datetime
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField


class AlertForm(FlaskForm):
    email = StringField('Email')
    message = TextAreaField("Email Message")
    alert_date = DateTimeField("Alert Date")
    submit = SubmitField('Create Alert')
