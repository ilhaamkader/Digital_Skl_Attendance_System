from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, validators, EmailField, UsernameField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField, TextAreaField
from wtforms.validators import EqualTo, DataRequired, Email, Length, Regexp

class Config(FlaskForm):
    email = EmailField('Email', validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')

class Login(FlaskForm):
    username = UsernameField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class ForgotPassword(FlaskForm):
    email = EmailField('Email', validators=[validators.Email(), validators.DataRequired()])
    submit = SubmitField('Submit')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    confirm = BooleanField('Confirm', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class AddSecretaryForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    rsa_id_num = StringField('RSA ID Number', validators=[
        DataRequired(), 
        Regexp(r'^\d{13}$', message='RSA ID must be exactly 13 digits')
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    cell_number = StringField('Cell Number', validators=[
        DataRequired(), 
        Regexp(r'^\d{10}$', message='Cell number must be exactly 10 digits')
    ])
    submit = SubmitField('Add Secretary')
