from pathlib import Path
from flask import current_app
from pathlib import Path
from datetime import datetime
import logging
import json
import re


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


'''

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


def update_grade_division_json(student):
    filename = f"{student.grade}{student.division}.json"
    filepath = os.path.join('json_data', filename)

    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append({
        'first_name': student.first_name,
        'last_name': student.last_name,
        'id_num': student.id_num
    })

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


def update_parent_json(student):
    parent = Parents.query.get(student.guardian_id)
    class_row = Class.query.get(student.class_id)
    grade = class_row.grade.grade_name
    division = class_row.division.division_name

    filename = f"parent_{student.guardian_id}.json"
    filepath = os.path.join('json_data', filename)

    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append({
        'first_name': student.first_name,
        'last_name': student.last_name,
        'id_num': student.id_num,
        'grade': grade,
        'division': division
    })

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)'''

#        .--.       .--.
#    _  `    \     /    `  _
#     `\.===. \.^./ .===./`
#            \/`"`\/
#        ,  |      |  ,
#       / `\|;-.-'|/` \
#       /    |::\  |    \
#   .-' ,-'`|:::; |`'-, '-.
#       |   |::::\|   | 
#       |   |::::;|   |
#       |   \:::://   |
#       |    `.://'   |
#jgs    .'             `.
#    _,'                 `,_