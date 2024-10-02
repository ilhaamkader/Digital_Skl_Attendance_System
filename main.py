from flask import Flask, jsonify, redirect, session, url_for, request, flash, render_template, current_app
from units import db, init_app, forms
from units.dao import AdminDAO, UserDAO, SecretaryDAO, EducatorDAO, GuardianDAO, SchoolClassDAO#, DatabaseUtilityDAO  Added UserDAO for login
from units.models import Admin, Secretary, Educator, Guardian, Student, SchoolClass, AttendanceRecord
from flask_login import login_user, logout_user, login_required, current_user
from units.utilities import save_config_data, is_configured, generate_username, role_required, generate_password, read_json_file#, update_grade_division_json, update_parent_json
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError
import os

from werkzeug.security import generate_password_hash

app = Flask(__name__, instance_relative_config=True)

def initialize_server():
    # Ensure the instance folder is created at the root level
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Configure the app to store the SQLite database in the root instance folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'project.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SECRET_KEY'] = 'super secret string'
    
    # Initialize the database and import models
    init_app(app)

    # Create the database and tables if they do not exist
    with app.app_context():
        db.create_all()

    # Add a basic route
    return app
    

CONFIG_FILE = os.path.join(app.instance_path, 'app_config.json')
os.makedirs(app.instance_path, exist_ok=True)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'digitalattendance05@gmail.com'
app.config["MAIL_PASSWORD"] = 'mtrz tebu zxes feiy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True    
mail = Mail(app) 




# General routes --------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    if not is_configured():
        return redirect(url_for('setup'))
    return redirect(url_for('login'))

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if is_configured():
        return redirect(url_for('login'))
    
    form = forms.Config()

    if form.validate_on_submit():
        email = form.email.data
        raw_password = form.password.data
        username = generate_username(email, 'admin')
        hashed_password = generate_password_hash(raw_password)

        school_name = form.school_name.data
        grade_range_start = form.grade_range_start.data
        grade_range_end = form.grade_range_end.data
        division_range_start = form.division_range_start.data
        division_range_end = form.division_range_end.data
        
        AdminDAO.add_admin(username=username, password=hashed_password, email=email)

        config_data = {
            'school_name': form.school_name.data,
            'grade_range': list(range(grade_range_start, grade_range_end + 1)),
            'division_range': [
                chr(i) for i in range(
                    ord(division_range_start.upper()), 
                    ord(division_range_end.upper()) + 1
                )
            ]
        }

        save_config_data(config_data)

        flash('Setup completed successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('setup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        user = UserDAO.get_user_by_username(username)

        if user:
            print(f"User found: {user.username}")
            if UserDAO.check_password(user, password):
                login_user(user)

                prefix = username[0].lower()
                session['user_type'] = prefix  # Store user role in the session

                if prefix == 'a':
                    flash('Welcome Admin!', 'success')
                    return redirect(url_for('admin_dashboard'))
                elif prefix == 's':
                    flash('Welcome Secretary!', 'success')
                    return redirect(url_for('secretary_dashboard'))
                elif prefix == 'e':
                    flash('Welcome Educator!', 'success')
                    return redirect(url_for('educator_dashboard'))
                elif prefix == 'p':
                    flash('Welcome Parent!', 'success')
                    return redirect(url_for('parent_dashboard'))
                else:
                    flash('Unknown user type. Please contact support.', 'warning')
                    return redirect(url_for('login'))
            else:
                flash('Invalid username or password.', 'danger')
                print("Password incorrect.")
        else:
            flash('Invalid username or password.', 'danger')
            print("User not found.")

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/manage_profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    username = current_user.username
    user = None
    role = None

    # Determine user role based on username prefix and query the correct field
    if username.startswith('a'):
        user = Admin.query.filter_by(username=username).first()
        role = 'admin'
    elif username.startswith('s'):
        user = Secretary.query.filter_by(username=username).first()
        role = 'secretary'
    elif username.startswith('e'):
        user = Educator.query.filter_by(username=username).first()
        role = 'educator'
    elif username.startswith('p'):
        user = Guardian.query.filter_by(username=username).first()
        role = 'parent'
    else:
        flash('Invalid user role or username', 'danger')
        return redirect(url_for('home'))

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('home'))

    # Instantiate the form
    form = forms.ManageProfileForm()

    if form.validate_on_submit():
        # Handle Change Password
        if form.change_password.data:
            current_password = form.current_password.data
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            # Determine the correct password field based on role
            if role == 'admin':
                password_field = user.password
            elif role == 'secretary':
                password_field = user.password
            elif role == 'educator':
                password_field = user.password
            elif role == 'parent':
                password_field = user.password
            else:
                password_field = None

            if not password_field or not check_password_hash(password_field, current_password):
                flash("Current password is incorrect", "danger")
            elif new_password != confirm_password:
                flash("New password and confirmation don't match", "danger")
            else:
                # Update the password based on role
                if role == 'admin':
                    user.password = generate_password_hash(new_password)
                elif role == 'secretary':
                    user.password = generate_password_hash(new_password)
                elif role == 'educator':
                    user.password = generate_password_hash(new_password)
                elif role == 'parent':
                    user.password = generate_password_hash(new_password)
                db.session.commit()
                flash("Password updated successfully", "success")

        # Handle Update Mobile Number
        if form.update_mobile.data and role in ['secretary', 'educator', 'parent']:
            new_mobile_number = form.mobile_number.data
            user.cell_number = new_mobile_number
            db.session.commit()
            flash("Mobile number updated successfully", "success")

        return redirect(url_for('manage_profile'))

    return render_template('manage_profile.html', user=user, role=role, form=form)


# Admin routes ----------------------------------------------------------------------------------------------------

@app.route('/admin_dashboard')
@role_required('a')  # Only admin users can access this page
def admin_dashboard():
    return render_template('admin_dashboard.html') 

@app.route('/add_secretary', methods=['GET', 'POST'])
@role_required('a')  # Assuming 'admin' is the role stored in session for admins
def add_secretary():
    form = forms.AddSecretaryForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        rsa_id_num = form.rsa_id_num.data
        email = form.email.data
        cell_number = form.cell_number.data

        username = generate_username(email, 'secretary')
        password = generate_password()
        hashed_password = generate_password_hash(password)

        SecretaryDAO.add_secretary(
            first_name=first_name,
            last_name=last_name,
            rsa_id_num=rsa_id_num,
            email=email,
            cell_number=cell_number,
            username=username,
            password=hashed_password
        )

        # Create a welcome email for the new secretary
        msg = Message(subject="Welcome to the System - Your Account Details",
                      sender='digitalattendance05@gmail.com',
                      recipients=[email])
        msg.body = (f"Hello {first_name} {last_name},\n\n"
                    f"Your account has been created. Below are your login details:\n\n"
                    f"Username: {username}\n"
                    f"Password: {password} (Please change this after logging in)\n\n"
                    "Thank you.")
        mail.send(msg)

        flash('Secretary successfully added and email sent.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_secretary.html', form=form)

@app.route('/add_educator', methods=['GET', 'POST'])
@role_required('a')
def add_educator():
    form = forms.AddEducatorForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        rsa_id_num = form.rsa_id_num.data
        email = form.email.data
        cell_number = form.cell_number.data

        username = generate_username(email, 'educator')
        password = generate_password()
        hashed_password = generate_password_hash(password)

        EducatorDAO.add_educator(
            first_name=first_name,
            last_name=last_name,
            rsa_id_num=rsa_id_num,
            email=email,
            cell_number=cell_number,
            username=username,
            password=hashed_password
        )

        msg = Message(subject="Welcome to the System - Your Account Details",
                    sender='digitalattendance05@gmail.com',
                    recipients=[email])
        msg.body = (f"Hello {first_name} {last_name},\n\n"
                    f"Your account has been created. Below are your login details:\n\n"
                    f"Username: {username}\n"
                    f"Password: {password} (Please change this after logging in)\n\n"
                    "Thank you.")
        mail.send(msg)

        flash('Educator successfully added and email sent.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_educator.html', form=form)

# Add a route to test DAO methods
@app.route('/admins', methods=['GET'])
@login_required
def get_admins():
    if isinstance(current_user, Admin):
        admins = AdminDAO.get_all_admins()
        return jsonify([{"id": admin.admin_id, "username": admin.username} for admin in admins])
    else:
        return jsonify({"error": "Access forbidden"}), 403



# Secretary routes ------------------------------------------------------------------------------------------------
@app.route('/secretary_dashboard')
@role_required('s')
def secretary_dashboard():
    return render_template('secretary_dashboard.html')

@app.route('/add_class', methods=['GET', 'POST']) # the validation of 1 educator per a class needs to be implemented
@role_required('s')
def add_class():
    form = forms.AddSchoolClass()

    config_data = read_json_file(CONFIG_FILE)
    grades = config_data.get('grade_range', [])
    divisions = config_data.get('division_range', [])

    # Populate form choices
    form.grade.choices = [(grade, f"Grade {grade}") for grade in grades]  # Convert grades to strings for display
    form.division.choices = [(division, division) for division in divisions]
    educators = Educator.query.all()
    form.educator.choices = [(educator.educator_id, educator.first_name) for educator in educators]

    if form.validate_on_submit():
        selected_grade = form.grade.data
        selected_division = form.division.data
        selected_educator_id = form.educator.data

        # Optionally, validate that the selected educator exists
        educator = Educator.query.get(selected_educator_id)
        if not educator:
            flash('Selected educator does not exist.')
            return redirect(url_for('add_class'))

        # Initialize class_students as an empty dictionary
        class_students = {}  # You can modify this based on your application's requirements

        try:
            SchoolClassDAO.add_class(
                educator_id=selected_educator_id,
                grade=selected_grade,
                division=selected_division,
                class_students=class_students
            )
            flash(f'Class Grade {selected_grade} Division {selected_division} added with teacher {educator.name}!')
            return redirect(url_for('secretary_dashboard'))  # Redirect to secretary_dashboard after success
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            flash(f'An error occurred while adding the class: {str(e)}')
            return redirect(url_for('add_class'))

    return render_template('add_class.html', form=form)


@app.route('/add_parent', methods=['GET', 'POST'])
@role_required('s')
def add_parent():
    form = forms.AddParentForm()  

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        rsa_id_num = form.rsa_id_num.data
        email = form.email.data
        cell_number = form.cell_number.data
        address = f"{form.street_address.data}, {form.suburb.data}, {form.city.data}, {form.province.data}"


        username = generate_username(email, 'parent')
        password = generate_password()
        hashed_password = generate_password_hash(password)

        GuardianDAO.add_guardian(
            first_name=first_name,
            last_name=last_name,
            rsa_id_number=rsa_id_num,
            email=email,
            cell_number=cell_number,
            address=address,
            username=username,
            password=hashed_password
        )
        
        msg = Message(subject="Welcome to the System - Your Account Details",
                    sender='digitalattendance05@gmail.com',
                    recipients=[email])
        msg.body = (f"Hello {first_name} {last_name},\n\nYour account has been created. "
                    f"Below are your login details:\n\n"
                    f"Username: {username}\n"
                    f"Password: {password} (Please change this after logging in)\n\n"
                    "Thank you.")
        mail.send(msg)

        flash('Parent successfully added and email sent.', 'success')
        return redirect(url_for('secretary_dashboard'))

    return render_template('add_parent.html', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
@role_required('s')
def add_student():
    form = forms.AddStudentForm()

    # Populate the guardian choices
    form.guardian_id.choices = [
        (guardian.guardian_id, f"{guardian.first_name} {guardian.last_name}")
        for guardian in Guardian.query.order_by(Guardian.first_name, Guardian.last_name).all()
    ]
    
    # Populate the school class choices
    form.school_class_id.choices = [
        (school_class.class_id, f'Grade {school_class.grade} - Division {school_class.division}')
        for school_class in SchoolClass.query.order_by(SchoolClass.grade, SchoolClass.division).all()
    ]

    if form.validate_on_submit():
        # Add the student to the Student table
        new_student = Student(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            rsa_id_number=form.rsa_id_number.data.strip(),
            guardian_id=form.guardian_id.data
        )
        db.session.add(new_student)
        db.session.commit()

        #Logic for adding to dependents list
        # Retrieve the corresponding guardian using Session.get()
        guardian = db.session.get(Guardian, form.guardian_id.data)

        # Check if guardian exists
        if guardian is None:
            flash('Guardian not found.', 'error')
            return redirect(url_for('register_student'))

        # Ensure guardian_dependants_list is a dictionary
        if not isinstance(guardian.guardian_dependants_list, dict):
            guardian.guardian_dependants_list = {}

        # Initialize 'dependants' if it does not exist
        if 'dependants' not in guardian.guardian_dependants_list:
            guardian.guardian_dependants_list['dependants'] = []

        # Prepare the student's information, including the class ID
        class_id = form.school_class_id.data
        student_info = {
            'first_name': new_student.first_name,
            'last_name': new_student.last_name,
            'rsa_id_number': new_student.rsa_id_number,
            'class_id': class_id
        }

        existing_dependants = guardian.guardian_dependants_list['dependants']

        # Check for existing dependant with the same RSA ID number
        if any(dep['rsa_id_number'] == student_info['rsa_id_number'] for dep in existing_dependants):
            flash('A dependant with this RSA ID number already exists.', 'warning')
            return redirect(url_for('register_student'))

        # Append the new student info to the dependants list
        guardian.guardian_dependants_list['dependants'].append(student_info)
        print(f"Added new dependant: {student_info}")

        try:
            # Commit changes to the database
            db.session.commit()

            updated_guardian = db.session.get(Guardian, form.guardian_id.data)
            print(f"Updated guardian dependants: {updated_guardian.guardian_dependants_list}")
            flash('Dependant registered successfully!', 'success')

        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while registering the dependant.', 'error')
            print(f"Database commit failed: {e}")
            return redirect(url_for('register_student'))
        

        # Logic for adding to class
        # Retrieve the corresponding school class
        school_class = db.session.get(SchoolClass, form.school_class_id.data)

        # Add the student's info to the school class's student list
        if 'students' not in school_class.class_students:
            school_class.class_students['students'] = []
        school_class.class_students['students'].append(student_info)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('add_student'))

    return render_template('add_student.html', form=form)


@app.route('/update_attendance', methods=['GET', 'POST'])
def update_attendance():
    form = forms.UpdateAttendanceForm()

    form.grade.choices = [(grade.id, grade.name) for grade in Grades.query.all()]
    form.division.choices = [(division.id, division.name) for division in Divisions.query.all()]

    if request.method == 'POST' and form.grade.data and form.division.data:
        class_id = f"{form.grade.data}{form.division.data}"
        students = Students.query.filter_by(grade=form.grade.data, division=form.division.data).all()
        form.student_id.choices = [(student.id, f"{student.first_name} {student.last_name}") for student in students]
        
    if form.validate_on_submit():
        date_str = form.date.data.strftime('%Y-%m-%d')
        class_id = f"{form.grade.data}{form.division.data}"
        filename = f"{date_str}_{class_id}_attendance.json"
        filepath = os.path.join('attendance_records', filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                attendance_data = json.load(file)

            for student_record in attendance_data:
                if student_record['student_id'] == form.student_id.data:
                    student_record['attendance_status'] = form.attendance_status.data
                    break

            with open(filepath, 'w') as file:
                json.dump(attendance_data, file, indent=4)

            flash('Attendance updated successfully.', 'success')
            return redirect(url_for('secretery_dashboard'))
        else:
            flash('Attendance record not found for the selected class and date.', 'danger')

    return render_template('update_attendance.html', form=form)


# Educator routes --------------------------------------------------------------------------------------------------
@app.route('/educator_dashboard')
@role_required('e')
def educator_dashboard():
    return render_template('educator_dashboard.html')


@app.route('/generate_class_list', methods=['GET', 'POST'])
def generate_class_list():
    form = forms.GenerateClassListForm()

    # Populate Grade and Division dropdowns
    form.grade.choices = [(grade.id, grade.name) for grade in Grades.query.all()]
    form.division.choices = [(division.id, division.name) for division in Divisions.query.all()]

    if form.validate_on_submit():
        date = form.date.data
        grade = form.grade.data
        division = form.division.data

        # Generate class list based on selected Grade and Division
        class_id = f"{grade}{division}"
        class_info = Class.query.filter_by(grade=grade, division=division).first()
        
        # Fetch form educator for the class
        form_educator = class_info.form_educator

        # Generate attendance register for the day (create JSON if not exists)
        date_str = date.strftime('%Y-%m-%d')
        filename = f"{date_str}_{class_id}_attendance.json"
        filepath = os.path.join('attendance_records', filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                attendance_data = json.load(file)
        else:
            # Create a new register for the class
            attendance_data = generate_daily_attendance(date, grade, division)

            # Save it to a JSON file
            with open(filepath, 'w') as file:
                json.dump(attendance_data, file, indent=4)

        # Redirect to the class list page to mark attendance
        return redirect(url_for('mark_attendance', date=date_str, class_id=class_id))

    return render_template('generate_class_list.html', form=form)



# Parent routes ---------------------------------------------------------------------------------------------------
@app.route('/parent_dashboard')
@role_required('p')  # Only admin users can access this page
def parent_dashboard():
    return render_template('parent_dashboard.html') 
   

@app.route('/add_attendance_exemption', methods=['GET', 'POST'])
def add_attendance_exemption():
    form = forms.ExemptionForm()

    form.grade.choices = [(grade.id, grade.name) for grade in Grades.query.all()]
    form.division.choices = [(division.id, division.name) for division in Divisions.query.all()]

    if form.grade.data and form.division.data:
        form.student_id.choices = [(student.id, f"{student.first_name} {student.last_name}") 
                                   for student in Students.query.filter_by(grade=form.grade.data, division=form.division.data).all()]

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        grade = form.grade.data
        division = form.division.data
        student_id = form.student_id.data
        reason = form.reason.data

        student = Students.query.get(student_id)
        class_id = f"{grade}{division}"

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            filename = f"{date_str}_{class_id}_attendance.json"
            filepath = os.path.join('attendance_records', filename)

            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    attendance_data = json.load(file)
            else:
                attendance_data = generate_daily_attendance(current_date, grade, division)

            for student_record in attendance_data:
                if student_record['student_id'] == student_id:
                    student_record['attendance_status'] = 'Exempted'
                    student_record['exemption_status'] = reason
                    break

            with open(filepath, 'w') as file:
                json.dump(attendance_data, file, indent=4)

            current_date += timedelta(days=1)

        flash('Exemption successfully added.', 'success')
        return redirect(url_for('secretary_dashboard'))

    return render_template('add_attendance_exemption.html', form=form)

 


if __name__ == "__main__":
    app = initialize_server()
    '''
    with app.app_context():
        DatabaseUtilityDAO.execute_sql_script("static/script.sql")
    '''
    
    app.run(debug=True)