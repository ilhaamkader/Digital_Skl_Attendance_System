from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, validators, EmailField, SelectField, DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField, TextAreaField
from wtforms.validators import EqualTo, DataRequired, Email, Length, Regexp, NumberRange

class Config(FlaskForm):
    email = StringField('Admin Email', validators=[DataRequired(), Email()])
    password = PasswordField('Admin Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(),EqualTo('password', message='Passwords must match')])

    school_name = StringField('School Name', validators=[DataRequired()])

    grade_range_start = IntegerField(
        'Grade Range Start', 
        validators=[DataRequired(), NumberRange(min=1, max=12)]
    )
    grade_range_end = IntegerField(
        'Grade Range End', 
        validators=[DataRequired(), NumberRange(min=1, max=12)]
    )
    division_range_start = StringField(
        'Division Range Start', 
        validators=[DataRequired(), Length(min=1, max=1)]
    )
    division_range_end = StringField(
        'Division Range End', 
        validators=[DataRequired(), Length(min=1, max=1)]
    )
    submit = SubmitField('Submit')


class Login(FlaskForm):
    username = EmailField('Username', validators=[validators.DataRequired()])
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

class AddParentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    rsa_id_num = StringField('RSA ID Number', validators=[DataRequired(), Length(min=13, max=13)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    cell_number = StringField('Cell Number', validators=[DataRequired(), Length(min=10, max=10)])

    street_address = StringField('Street Address', validators=[DataRequired(), Length(min=5, max=100)])
    suburb = StringField('Suburb', validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    province = SelectField('Province', choices=[
        ('Gauteng', 'Gauteng'),
        ('Western Cape', 'Western Cape'),
        ('KwaZulu-Natal', 'KwaZulu-Natal'),
        ('Eastern Cape', 'Eastern Cape'),
        ('Free State', 'Free State'),
        ('Limpopo', 'Limpopo'),
        ('Mpumalanga', 'Mpumalanga'),
        ('Northern Cape', 'Northern Cape'),
        ('North West', 'North West')
    ], validators=[DataRequired()])

    submit = SubmitField('Add Parent')


class AddStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    id_num = StringField('ID Number', validators=[DataRequired(), Length(min=13, max=13)])
    guardian = SelectField('Guardian', choices=[], coerce=int, validators=[DataRequired()])
    grade = SelectField('Grade', choices=[], validators=[DataRequired()])
    division = SelectField('Division', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Student')

class ExemptionForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    grade = SelectField('Grade', choices=[], validators=[DataRequired()])
    division = SelectField('Division', choices=[], validators=[DataRequired()])
    student_id = SelectField('Student ID', choices=[], validators=[DataRequired()])
    reason = TextAreaField('Reason for Exemption', validators=[DataRequired()])
    submit = SubmitField('Update Attendance')

class GenerateClassListForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    grade = SelectField('Grade', choices=[], validators=[DataRequired()])
    division = SelectField('Division', choices=[], validators=[DataRequired()])
    submit = SubmitField('Generate List')
