from functools import wraps
from pathlib import Path
from flask import current_app, session, redirect, url_for, flash
from pathlib import Path
from datetime import datetime
import string
from random import choice, shuffle
from sqlalchemy import event
from sqlalchemy.orm import Session
import json
import re
import os

from units.models import Student


def save_config_data(config_data):
    """
    Save the configuration data to app_config.json in the instance folder.
    
    Args:
        config_data (dict): The configuration data to save.
    """
    config_filename = 'app_config.json'
    config_path = Path(current_app.instance_path) / config_filename

    # Ensure the instance folder exists
    Path(current_app.instance_path).mkdir(parents=True, exist_ok=True)

    # Add the date_created field if not present
    if 'date_created' not in config_data:
        config_data['date_created'] = datetime.utcnow().isoformat()

    try:
        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        current_app.logger.info(f"Config file saved successfully: {config_data}")
    except Exception as e:
        current_app.logger.error(f"Error saving config: {e}")
        raise


def load_config_data():
    """
    Load the configuration data from app_config.json in the instance folder.

    Returns:
        dict: The configuration data.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file contains invalid JSON.
    """
    config_filename = 'app_config.json'
    config_path = Path(current_app.instance_path) / config_filename

    if not config_path.is_file():
        raise FileNotFoundError("Configuration file not found. Please run the setup first.")

    try:
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
        current_app.logger.info("Config file loaded successfully.")
        return config_data
    except json.JSONDecodeError as e:
        current_app.logger.error(f"Invalid JSON in config file: {e}")
        raise
    except Exception as e:
        current_app.logger.error(f"Error loading config: {e}")
        raise



def is_configured():
    """
    Check if the configuration file exists in the instance folder.
    
    Returns:
        bool: True if the config file exists, False otherwise.
    """
    config_filename = 'app_config.json'
    config_path = Path(current_app.instance_path) / config_filename
    return config_path.is_file()


def generate_username(email, user_type):
    email_prefix = re.split('@', email)[0]

    if user_type == 'admin':
        prefix = 'a'

    elif user_type == 'secretary':
        prefix = 's'

    elif user_type == 'parent':
        prefix = 'p'
    
    elif user_type == 'educator':
        prefix = 'e'

    else:
        raise ValueError("Invalid user type")

    username = f"{prefix}{email_prefix}"
    return username

# All code above has been tested and is safe

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the user is logged in and has the required role
            if 'user_type' not in session or session['user_type'] != role:
                flash('You do not have permission to access this page.')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def generate_password():
    # Specify counts for letters, numbers, and symbols
    Letter_Count = 8  # Example: 8 letters
    Number_Count = 4  # Example: 4 numbers
    Symbol_Count = 2  # Example: 2 symbols

    Password_List = []
    # Generate letters
    for L in range(Letter_Count):
        Password_List.append(choice(string.ascii_letters))
    # Generate numbers
    for N in range(Number_Count):
        Password_List.append(choice(string.digits))
    # Generate symbols
    for S in range(Symbol_Count):
        Password_List.append(choice(string.punctuation))

    # Shuffle the password list
    shuffle(Password_List)

    # Concatenate the characters to form the password
    Randomised_String = ''.join(Password_List)
    return Randomised_String



# read config json file for Grade and Division
def read_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def generate_daily_attendance(date, grade, division):
    class_id = f"{grade}{division}"
    filename = f"{date}_{class_id}_attendance.json"
    filepath = os.path.join('attendance_records', filename)

    if not os.path.exists(filepath):
        students = Students.query.filter_by(grade=grade, division=division).all()
        attendance_data = []

        for student in students:
            attendance_data.append({
                'student_id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'attendance_status': 'Absent',
                'exemption_status': 'None'
            })

        with open(filepath, 'w') as file:
            json.dump(attendance_data, file, indent=4)

    return filepath
    
def get_logged_in_parent_id():
    
    if session.get('user_type') == 'p' and 'guardian_id' in session:
        return session['guardian_id']
    return None 