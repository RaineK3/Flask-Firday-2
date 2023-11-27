from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

#create search form
class searchForm(FlaskForm):
  searched = StringField("Searched", validators=[DataRequired()])
  submit = SubmitField("Submit")

#create login form
class loginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Submit")

#create a post form 
class PostForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  #content = StringField("Content", validators=[DataRequired()], widget=TextArea())
  #content = CKEditorField("Content", validators=[DataRequired()])
  content = CKEditorField('Content',validators=[DataRequired()])
  author = StringField("Author")
  slug = StringField("Slug", validators=[DataRequired()])
  submit = SubmitField("Submit")

#create a Form Class
class UserForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  username = StringField("Username", validators=[DataRequired()]) 
  email = StringField("Email", validators=[DataRequired()]) 
  favorite_color = StringField("Favorite Color") 
  about_author = TextAreaField("About Author") 
  password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match.')])
  password_hash2 = PasswordField('Comfirm Password', validators=[DataRequired()])
  profile_pic = FileField("Porfile Picture")
  submit = SubmitField("Submit")

#create a class form 
class PasswordForm(FlaskForm):
  email = StringField("What's your email?", validators=[DataRequired()]) 
  password_hash = PasswordField("What's your password?", validators=[DataRequired()])
  submit = SubmitField("Submit")


#create a name form
class NameForm(FlaskForm):
  name = StringField("What's your name?", validators=[DataRequired()]) 
  submit = SubmitField("Submit")