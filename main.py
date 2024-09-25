from flask import Flask, jsonify
from units import db, init_app
from units.dao import AdminDAO
import os

app = None

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder is created at the root level
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Configure the app to store the SQLite database in the root instance folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'project.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and import models
    init_app(app)

    # Create the database and tables if they do not exist
    with app.app_context():
        db.create_all()

    return app
    # Add a basic route

@app.route('/')
def home():
    return jsonify(message="Welcome to the Security App")

# Add a route to test DAO methods
@app.route('/admins', methods=['GET'])
def get_admins():
    admins = AdminDAO.get_all_admins()
    return jsonify([{"id": admin.admin_id, "username": admin.admin_username} for admin in admins])

    

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
