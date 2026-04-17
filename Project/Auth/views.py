from Project.Auth import bp
from Project.Auth.forms.signupf import SignUp
from Project.Auth.forms.signin import SignIn
from flask import render_template,flash,redirect,url_for
from Project.Models import User
from Project import db
from flask_login import login_user,logout_user,login_required

@bp.route("/signup",methods=["POST","GET"])
def signup():
    form = SignUp()
    if form.validate_on_submit():
        fname = form.firstName.data
        lname = form.lastName.data
        email = form.Email.data
        password = form.Password.data
        major = form.major.data
        user = User(fname,lname,email,major,password,'عدل البايو')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('Auth.signin'))
    return render_template("signup.html",form=form)

@bp.route('/signin',methods=["POST","GET"])
def signin():
    signin = SignIn()
    if signin.validate_on_submit():
        email = signin.Email.data
        password = signin.Password.data
        if User.query.filter_by(email=email):
            user = User.query.filter_by(email=email).first()
            if user and user.checkpass(password):
                flash("Signed In")
                login_user(user)                
                return redirect(url_for('Home.index'))
            else:
                return "invalid credentials"
    return render_template('signin.html',form=signin)

@bp.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('Home.index'))