from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, TextAreaField, SelectMultipleField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class EditorForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=250)])
    body = PageDownField('Body', validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int)
    timestamp = DateTimeField('Timestamp')
    published = BooleanField('Publish?')
    update = BooleanField('Update Timestamp?')
    submit = SubmitField('Save')
