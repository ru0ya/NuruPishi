#!/usr/bin/python3
"""user validation forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    InputRequired,
    Regexp,
    EqualTo,
    Optional
)
from email_validator import validate_email, EmailNotValidError

from nurupishi.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField('Email', 
                        validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpassword = PasswordField('Confirm Password',
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("password", message="Passwords must match!"),
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """
        validates if a users email is already registered
        """
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        """
        validates if users username is taken
        """
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken")

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField('Password',
        validators=[InputRequired(), Length(min=8, max=72)])
    username = StringField('Username',
        validators=[Optional()]
    )
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
     email = StringField('Email' ,
                         validators=[InputRequired(), Email(), Length(1, 64)])
     submit = SubmitField('Request Password Reset')

     def validate_email(self, email):
         """
         validates users email to allow for account details changing
         if account does not exist, user has to register
         """
         user = User.query.filter_by(email=email.data).first()
         password = PasswordField(validators=[InputRequired(), Length(8, 72)])
         cpassword = PasswordField('Confirm Password',
                                   validators=[
                                       InputRequired(),
                                       Length(8, 72),
                                       EqualTo("password", message="Passwords must match!"),
                                   ]
                                  )
         if user is None:
             raise ValidationError("There is no account with that email. You must register first")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    cpassword = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


