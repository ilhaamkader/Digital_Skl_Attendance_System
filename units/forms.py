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
        validators=[DataRequired(), NumberRange(min=0, max=12)] #min can not be 0 app doesnot work if its 0
    )
    grade_range_end = IntegerField(
        'Grade Range End', 
        validators=[DataRequired(), NumberRange(min=0, max=12)]
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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    forgot_username = SubmitField('Forgot Username')
    forgot_password = SubmitField('Forgot Password')
    login = SubmitField('Login')


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

class AddEducatorForm(FlaskForm):
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
    submit = SubmitField('Add Educator')


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

class AddSchoolClass(FlaskForm):
    educator = SelectField('Educator', choices=[], validators=[DataRequired()])
    grade = SelectField('Grade', choices=[], validators=[DataRequired()])
    division = SelectField('Division', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Class')

class AddStudentForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message="First name is required."),
            Length(max=100, message="First name cannot exceed 100 characters.")
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message="Last name is required."),
            Length(max=100, message="Last name cannot exceed 100 characters.")
        ]
    )
    rsa_id_number = StringField(
        'RSA ID Number',
        validators=[
            DataRequired(message="RSA ID number is required."),
            Length(min=13, max=13, message="RSA ID number must be exactly 13 characters."),
            Regexp(r'^\d{13}$', message="RSA ID number must contain only digits.")
        ]
    )
    guardian_id = SelectField(
        'Guardian',
        coerce=int,
        validators=[DataRequired(message="Please select a parent/guardian.")]
    )
    school_class_id = SelectField(
        'Grade and Division',
        coerce=int,
        validators=[DataRequired(message="Please select a grade and division.")]
    )
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

class ManageProfileForm(FlaskForm):
    current_password = PasswordField('Current Password', 
                                     validators=[DataRequired()])
    
    new_password = PasswordField('New Password', 
                                 validators=[DataRequired(), 
                                             Length(min=6, max=50, message="Password must be between 6 and 50 characters.")])
    
    confirm_password = PasswordField('Confirm New Password', 
                                     validators=[DataRequired(), 
                                                 EqualTo('new_password', message="Passwords must match.")])
    
    # Update Mobile Number Section (conditional on role)
    mobile_number = StringField('Mobile Number', 
                                validators=[Regexp(r'^\d{10}$', 
                                                   message="Mobile number must be exactly 10 digits.")])
    
    # Submit buttons
    change_password = SubmitField('Change Password')
    update_mobile = SubmitField('Update Mobile Number')