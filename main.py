from flask import Flask, jsonify, redirect, url_for, request, flash, render_template
from units import db, init_app
from units.dao import AdminDAO, UserDAO, DatabaseUtilityDAO  # Added UserDAO for login
from flask_login import login_user, logout_user, login_required, current_user
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

@app.route('/')
def home():
    if current_user.is_authenticated:
        return f"<h1>Welcome, {current_user.username}</h1>"
    return "<h1>Welcome, Guest</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Use the DAO to get the user and check password
        user = UserDAO.get_user_by_username(username)

        if user and UserDAO.check_password(user, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

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
