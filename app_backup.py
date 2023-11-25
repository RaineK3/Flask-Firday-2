from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#create a flask instance 
app = Flask(__name__)
#add database
#sqlite db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:raine@localhost/our_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#secret key
app.config['SECRET_KEY'] = "I'm so handsome"
#initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

app.app_context().push()

#flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))

#create login form
class loginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Submit")
  
#create a post model
class Posts(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))
  content = db.Column(db.Text)
  author = db.Column(db.String(255))
  date_posted = db.Column(db.DateTime, default = datetime.utcnow)
  slug = db.Column(db.String(255))

#create user model
class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(20), nullable = False, unique = True)
  name = db.Column(db.String(200), nullable = False)
  email = db.Column(db.String(120), nullable = False, unique = True)
  favorite_color = db.Column(db.String(200))
  date_added = db.Column(db.DateTime, default = datetime.utcnow)
  #do some password stuff!
  password_hash = db.Column(db.String(128))
  @property
  def password(self):
    raise AttributeError("Password is not a readable attribute!")
  
  @password.setter
  def password(self,password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self,password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<Name %r>' % self.name

#create a post form 
class PostForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  content = StringField("Content", validators=[DataRequired()], widget=TextArea())
  author = StringField("Author", validators=[DataRequired()])
  slug = StringField("Slug", validators=[DataRequired()])
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

#create a Form Class
class UserForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  username = StringField("Username", validators=[DataRequired()]) 
  email = StringField("Email", validators=[DataRequired()]) 
  favorite_color = StringField("Favorite Color") 
  password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match.')])
  password_hash2 = PasswordField('Comfirm Password', validators=[DataRequired()])
  submit = SubmitField("Submit")

#create individual post page
@app.route('/posts/<int:id>')
def post(id):
  post = Posts.query.get_or_404(id)
  return render_template('post.html', post = post)

@app.route('/posts')
def posts():
  #grab all the posts form the database
  posts = Posts.query.order_by(Posts.date_posted)
  return render_template("posts.html",
                         posts = posts)

@app.route('/posts/delete/<int:id>')
def delete_post(id):
  #get the post to delete from database
  post_to_delete = Posts.query.get_or_404(id)
  try:
    #delete the post from databae
    db.session.delete(post_to_delete)
    db.session.commit()
    flash("Blog post was deleted!!")
    #grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)

  except:
    flash("Whoops! There was a problem while deleting the post, Try again...")

    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)


@app.route('/posts/edit/<int:id>', methods= ['POST', 'GET'])
@login_required
def edit_post(id):
  post = Posts.query.get_or_404(id)
  form = PostForm()
  if form.validate_on_submit():
    #get data to update from form
    post.title = form.title.data
    post.author = form.author.data
    post.slug = form.slug.data
    post.content = form.content.data
    #update database
    db.session.add(post)
    db.session.commit()
    flash("Post has been updated!")
    return redirect(url_for('post',id = post.id))
  #fill the form from data fromd database
  form.title.data = post.title
  form.author.data = post.author
  form.slug.data = post.slug
  form.content.data = post.content
  return render_template('edit_post.html', form = form)

  
#create a post page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
  form = PostForm()

  if form.validate_on_submit():
    post = Posts(title=form.title.data,
                 content = form.content.data,
                 author = form.author.data,
                 slug = form.slug.data)
    #clear form 
    form.title.data = ''
    form.content.data = ''
    form.title.data = ''
    form.author.data = ''
    form.slug.data = ''
    #add post to the database
    db.session.add(post)
    db.session.commit()

    flash("Blog post submittted successfully!")
  #redirect to the webpage
  return render_template("add_post.html",
                           form = form)
 
#delete database record
@app.route('/delete/<int:id>')
def delete(id):
  user_to_delete = Users.query.get_or_404(id)
  name = user_to_delete.name
  form = UserForm()
  try:
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User Deleted Successfully!!")
    our_users = Users.query.order_by(Users.date_added)
  
    return render_template("add_user.html",
                         form = form,
                         name = name,
                         our_users = our_users)

  
  except:
    flash("Whoops! There was a problem while deleting data. Try again..")
    return render_template("add_user.html",
                         form = form,
                         name = name,
                         our_users = our_users)

#update database record
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
  form = UserForm()
  name_to_update = Users.query.get_or_404(id)
  if request.method == "POST":
    name_to_update.name = request.form['name']
    name_to_update.username = request.form['username']
    name_to_update.email = request.form['email']
    name_to_update.favorite_color = request.form['favorite_color']
    
    try:
      db.session.commit()
      flash("User Updated Successfully!")
      return render_template("update.html",
                             form = form,
                             name_to_update = name_to_update,
                             id = id)
    except:
      flash("Error! Looks like there was a problem.")
      return render_template("update.html",
                             form = form,
                             name_to_update = name_to_update,
                             id = id)
  else:
    return render_template("update.html",
                             form = form,
                             name_to_update = name_to_update,
                             id = id)



@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
  name = None
  form = UserForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      #hash the password!!
      # hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
      hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
      user = Users(name= form.name.data,username= form.username.data, email= form.email.data, favorite_color=form.favorite_color.data, password_hash = hashed_pw)
      db.session.add(user)
      db.session.commit()
    name = form.name.data
    form.name.data = ''
    form.username.data = ''
    form.email.data = ''
    form.favorite_color = ''
    form.password_hash = ''
    flash("User added successfully!!")
  our_users = Users.query.order_by(Users.date_added)
  
  return render_template("add_user.html",
                         form = form,
                         name = name,
                         our_users = our_users)

  
#create login page
@app.route('/login', methods = ['POST','GET'])
def login():
  form = loginForm()
  if form.validate_on_submit():
    #get the user by unique username
    user = Users.query.filter_by(username = form.username.data).first()
    if user:
      #check the password after hashing with hashed passsword
      if check_password_hash(user.password_hash,form.password.data):
        login_user(user)
        flash("Login successful!!")
        return redirect(url_for('dashboard'))
      else:
        flash("Wrong password - Try again!!!")
    else:
      flash("That user doesn't exit!!")
  return render_template('login.html', form = form)

#create logout page
@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
  logout_user()
  flash('You have been logged out!!')
  return redirect(url_for('login'))

#create dashboard page
@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
  form = UserForm()
  id = current_user.id
  name_to_update = Users.query.get_or_404(id)
  if request.method == "POST":
    name_to_update.name = request.form['name']
    name_to_update.username = request.form['username']
    name_to_update.email = request.form['email']
    name_to_update.favorite_color = request.form['favorite_color']
    
    try:
      db.session.commit()
      flash("User Updated Successfully!")
      return render_template("dashboard.html",
                             form = form,
                             name_to_update = name_to_update,
                             id = id)
    except:
      flash("Error! Looks like there was a problem.")
      return render_template("dashboard.html",
                             form = form,
                             name_to_update = name_to_update,
                             id = id)
  else:
    return render_template("dashboard.html",
                             form = form,
                             name_to_update = name_to_update,
                             id = id)
  
  # return render_template('dashboard.html')

#create a route decorator 
@app.route('/')
def index():
  flash("Welcome To Our Website!")
  return render_template("index.html")

@app.route('/user/<name>')
def user(name):
  return render_template("user.html", username = name)

#create custom error pages

#invalid url
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"),404

#internl server error
@app.errorhandler(500)
def page_not_found(e):
  return render_template("500.html"),500


#create password test page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
   email = None
   password = None
   pw_to_check = None
   passed = None
   form = PasswordForm()
  
   #validate form
   if form.validate_on_submit():
     email = form.email.data
     password = form.password_hash.data
     #clear form
     form.email.data = ''
     form.password_hash.data = ''
     #look for user by email address
     pw_to_check = Users.query.filter_by(email=email).first()
     #check hashed password
     passed = check_password_hash(pw_to_check.password_hash, password)
   return render_template("test_pw.html",
                          email = email,
                          password = password,
                          form = form,
                          pw_to_check = pw_to_check,
                          passed = passed)

#create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
   name = None
   form = NameForm()
   #validate form
   if form.validate_on_submit():
     name = form.name.data
     form.name.data = ''
     flash("Form Submitted Successfully!")
   return render_template("name.html",
                          name = name,
                          form = form)

# if __name__ == "__main__":
#     app.run(debug=True)