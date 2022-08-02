from flask import Blueprint, render_template, redirect, request, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user, LoginManager, UserMixin


auth = Blueprint('auth', __name__)


    


@auth.route('/login', methods=['POST', 'GET'])
def login():
    # login code goes here
    if request.method == 'POST':
      email = request.form.get('email')
      password = request.form.get('password')
      remember = True if request.form.get('remember') else False

      user = User.query.filter_by(email=email).first()
      if user:
            if check_password_hash(user.password, password):
                  flash("Logged in successfully", category='success')
                  login_user(user, remember=remember)
                  return redirect('/')
            else:
                  flash("Incorrect password", category='error')
      else:
            flash('Email does not exist', category='error')

      
    return render_template('auth/login.html')



@auth.route('/logout')
@login_required
def logout():
      logout_user()
      flash('Succesfully logged out' , category='success')
      return redirect(url_for('views.home'))



@auth.route('/signup', methods= ['GET', "POST"])
def signup():
      if request.method == "POST":
            email  = request.form.get('email')
            name = request.form.get('name')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            if len(email) < 4:
                  flash('Please enter correct Email(more than 4 signs)', category='error')
            elif len(name)< 3:
                  flash('Your name was too short', category='error')
            elif password1 != password2:
                  flash ("Passwords don't  match", category='error')
            elif len(password1) < 6:
                  flash ("Passwords must be more than 6 characters ", category='error')
            else:
                  flash ('Account created', category='success' )
                  user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

                  if user: # if a user is found, we want to redirect back to signup page so user can try again
                        flash('Email address already exists')
                        return redirect(url_for('auth.signup'))
                  else:
                        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
                        new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))

                        # add the new user to the database
                        db.session.add(new_user)
                        db.session.commit()

                        return redirect(url_for('auth.login'))

      return render_template('auth/signup.html')