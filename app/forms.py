from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, SubmitField, StringField, TextAreaField, SelectMultipleField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField
from app import app


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class EditorForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=250)])
    image = FileField('Header Image', validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    blurb = TextAreaField('Blurb', validators=[Length(max=200)])
    body = PageDownField('Body', validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int, description="CTRL and click to unselect/select multiple tags")
    new_tags = StringField('New Tags', description="Separate new tags with a space")
    timestamp = DateTimeField('Timestamp')
    published = BooleanField('Publish?')
    update = BooleanField('Update Timestamp?')
    delete = SubmitField('Delete')
    submit = SubmitField('Save')
