from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user


auth=Blueprint('auth',__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
  if request.method=='POST':

    email=request.form.get('email')  #here email is the name of the field(name defined for field in login.html)
    password=request.form.get('password1')

    user=User.query.filter_by(email=email).first()

    if user:
      if check_password_hash(user.password,password):
        flash('logged in successfully !',category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password,try again',category='error')
    else:
      flash('Email does not exist',category='error')

  return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET','POST'])
def signin():
  if request.method =="POST":
    email=request.form.get('email')
    first_name=request.form.get('firstName')
    password1=request.form.get('password1')
    password2=request.form.get('password2')

    user=User.query.filter_by(email=email).first()

    if user:
      flash('email already exists',category='error')
    elif len(email) < 4:
      flash("invalid email address",category='error')
    elif first_name is None or len(first_name)< 2 :
      flash("first Name must be greater than 1 character",category='error')
    elif len(password1)<7:
      flash("password must be atleast 8 characters",category='error')
    elif password1 != password2:
      flash("confirmed password does not match",category='error')
    else:
      new_user=User(email =email,first_name=first_name,password=generate_password_hash(password1,method='pbkdf2:sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user,remember=True)

      flash("Account creation successful",category='success')
      return redirect(url_for('views.home'))
  return render_template("signin.html",user=current_user)
