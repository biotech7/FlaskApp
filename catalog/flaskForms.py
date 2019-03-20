from flask_wtf import FlaskForm
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalogDB import User, Base
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

# Connect to Database and create database session
engine = create_engine('sqlite:///site.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=45), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    signin = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    username = StringField("UserName", validators=[DataRequired(), Length(max=25)])
    email = StringField("Email", validators=[DataRequired(), Length(max=45), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    signup = SubmitField("Sign Up")

    def validate_username(self, username):
        user = session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

