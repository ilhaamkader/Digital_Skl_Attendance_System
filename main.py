from flask import Flask, jsonify, redirect, url_for, request, flash, render_template
from units import db, init_app
from units.dao import AdminDAO, UserDAO, DatabaseUtilityDAO  # Added UserDAO for login
from flask_login import login_user, logout_user, login_required, current_user
from units.forms import Config, Login, ForgotPassword, ResetPassword, AddSecretaryForm, AddParentForm, AddStudentForm, UpdateAttendanceForm, AddEducatorForm, ExemptionForm, GenerateClassListForm, ManageProfileForm, ChangePasswordForm
import os

app = Flask(__name__, instance_relative_config=True)

def initialize_server():
    # Ensure the instance folder is created at the root level
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Configure the app to store the SQLite database in the root instance folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'project.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'super secret string'
    
    # Initialize the database and import models
    init_app(app)

    # Create the database and tables if they do not exist
    with app.app_context():
        db.create_all()

    return app

@app.route('/', methods=['GET', 'POST'])
def setup():
    form = Config()
    if form.validate_on_submit():
        pass
    return render_template('setup.html', form=form)

# Config Page Route
@app.route('/config', methods=['GET', 'POST'])
def config():
    config_form = Config()
    if request.method == 'POST' and config_form.validate_on_submit():
        flash('Configuration updated successfully!', 'success')
        return redirect(url_for('config'))
    return render_template('config.html', form=config_form)

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login()
    if request.method == 'POST' and login_form.validate_on_submit():
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=login_form)

# Forgot Username/Password Route
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    forgot_form = ForgotPassword()
    if request.method == 'POST' and forgot_form.validate_on_submit():
        flash('Recovery email sent!', 'success')
        return redirect(url_for('login'))
    return render_template('forgot-user-pass.html', form=forgot_form)

# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html')

# Add Educator Route
@app.route('/add_educator', methods=['GET', 'POST'])
def add_educator():
    add_educator_form = AddEducatorForm()
    if request.method == 'POST' and add_educator_form.validate_on_submit():
        flash('Educator added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add-educator.html', form=add_educator_form)

# Add Secretary Route
@app.route('/add_secretary', methods=['GET', 'POST'])
def add_secretary():
    add_secretary_form = AddSecretaryForm()
    if request.method == 'POST' and add_secretary_form.validate_on_submit():
        flash('Secretary added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add-secretary.html', form=add_secretary_form)

# Manage Profile Route
@app.route('/manage_profile', methods=['GET', 'POST'])
def manage_profile():
    manage_profile_form = ManageProfileForm()
    if request.method == 'POST' and manage_profile_form.validate_on_submit():
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('manage_profile'))
    return render_template('manage-profile.html', form=manage_profile_form)

# Change Password Route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    change_password_form = ResetPassword()
    if request.method == 'POST' and change_password_form.validate_on_submit():
        flash('Password updated successfully!', 'success')
        return redirect(url_for('manage_profile'))
    return render_template('change-password.html', form=change_password_form)

# Secretary Dashboard Route
@app.route('/secretary_dashboard')
def secretary_dashboard():
    return render_template('secretary-dashboard.html')

# Add Parent/Guardian Route
@app.route('/add_parent_guardian', methods=['GET', 'POST'])
def add_parent_guardian():
    add_parent_guardian_form = AddParentForm()
    if request.method == 'POST' and add_parent_guardian_form.validate_on_submit():
        flash('Parent/Guardian added successfully!', 'success')
        return redirect(url_for('secretary_dashboard'))
    return render_template('add-parent-guardian.html', form=add_parent_guardian_form)

# Add Student Route
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    add_student_form = AddStudentForm()
    if request.method == 'POST' and add_student_form.validate_on_submit():
        flash('Student added successfully!', 'success')
        return redirect(url_for('secretary_dashboard'))
    return render_template('add-student.html', form=add_student_form)

# Update Attendance Route
@app.route('/update_attendance', methods=['GET', 'POST'])
def update_attendance():
    update_attendance_form = UpdateAttendanceForm()
    if request.method == 'POST' and update_attendance_form.validate_on_submit():
        flash('Attendance updated successfully!', 'success')
        return redirect(url_for('secretary_dashboard'))
    return render_template('update-attendance.html', form=update_attendance_form)

# Add Attendance Exemption Route
@app.route('/add_attendance_exemption', methods=['GET', 'POST'])
def add_attendance_exemption():
    add_attendance_exemption_form = ExemptionForm()
    if request.method == 'POST' and add_attendance_exemption_form.validate_on_submit():
        flash('Attendance exemption added successfully!', 'success')
        return redirect(url_for('secretary_dashboard'))
    return render_template('add-attendance-exemption.html', form=add_attendance_exemption_form)

# Educator Dashboard Route
@app.route('/educator_dashboard')
def educator_dashboard():
    return render_template('educator-dashboard.html')

# Generate Class List Route
@app.route('/generate_class_list', methods=['GET', 'POST'])
def generate_class_list():
    generate_class_list_form = GenerateClassListForm()
    if request.method == 'POST' and generate_class_list_form.validate_on_submit():
        flash('Class list generated successfully!', 'success')
        return redirect(url_for('educator_dashboard'))
    return render_template('generate-class-list.html', form=generate_class_list_form)

# Parent Dashboard Route
@app.route('/parent_dashboard')
def parent_dashboard():
    return render_template('parent-dashboard.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Add a route to test DAO methods
@app.route('/admins', methods=['GET'])
@login_required
def get_admins():
    if isinstance(current_user, Admin):
        admins = AdminDAO.get_all_admins()
        return jsonify([{"id": admin.admin_id, "username": admin.admin_username} for admin in admins])
    else:
        return jsonify({"error": "Access forbidden"}), 403

if __name__ == "__main__":
    app = initialize_server()
    
    with app.app_context():
        DatabaseUtilityDAO.execute_sql_script("static/script.sql")
    
    app.run(debug=True)
