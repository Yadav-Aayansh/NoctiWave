# /NoctiWave/app/user/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
from .admin.models import Admin
from .influencer.models import Influencer
from .sponsor.models import Sponsor
from .. import enc, db

class SignupForm(FlaskForm):
    role = RadioField("Get Started As", choices=[("admin", "Admin"), ("influencer", "Influencer"), ("sponsor", "Sponsor")], default="admin")
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[Email(message="Please enter a valid email address."), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("password", message="Password must be same."), DataRequired(), Length(min=8, max=20)])
    submit = SubmitField("Signup to Continue")

    def validate_username(self, username):
        allowed = "-_."
        username.data = username.data.lower()
        if all(char.isalnum() or char in allowed for char in username.data):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This Username is already taken!")
        else:
            raise ValidationError("Username contains invalid characters.")
        
    def validate_email(self, email):
        email.data = email.data.lower()
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Address is already in use.")
        
    def registration(self):
        if self.validate():
            hashed_password = enc.generate_password_hash(self.password.data)
            new_user = User(username=self.username.data, email=self.email.data, password=hashed_password, role=self.role.data)
            db.session.add(new_user)
            db.session.commit()
            if self.role.data == "admin":
                new_role = Admin(user_id=new_user.user_id)
            elif self.role.data == "influencer":
                new_role = Influencer(user_id=new_user.user_id)
            elif self.role.data == "sponsor":
                new_role = Sponsor(user_id=new_user.user_id)
            db.session.add(new_role)
            db.session.commit()
            session["user_id"] = new_user.user_id
            return True
        return False
        

class LoginForm(FlaskForm):
    user_mail = StringField("Username or Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login to Your Account")

    def logar(self):
        if self.validate():
            self.user_mail.data = self.user_mail.data.lower()
            user = User.query.filter((User.email==self.user_mail.data)|(User.username==self.user_mail.data)).first()
            if user is None:
                return "NOT-FOUND"
            elif user and enc.check_password_hash(user.password, self.password.data):
                session["user_id"] = user.user_id
                if self.remember.data:
                    session.permanent = True
                return True
            else:
                return False


auth_bp = Blueprint("auth_bp", __name__, template_folder="../templates/auth")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if "user_id" in session:
        return redirect(url_for("dashboard_bp.dashboard"))
    elif form.validate_on_submit():
        if form.registration():
            session['message'] = {"message": 'Account created successfully!'}
            return redirect(url_for("dashboard_bp.profile"))
        else:
            return render_template("signup.html", form=form)
    else:
        return render_template("signup.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if "user_id" in session:
        return redirect(url_for("dashboard_bp.dashboard"))
    elif form.validate_on_submit():
        result = form.logar()
        if result == True:
            return redirect(url_for("dashboard_bp.dashboard"))
        elif result == False:
            flash("Incorrect username or password!", "danger")
        elif result == "NOT-FOUND":
            flash("Sorry, Account does not exist!", "danger")
        else:
            return render_template("login.html", form=form)
        
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth_bp.login"))