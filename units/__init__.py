from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    # Import models only after app is initialized to avoid circular import issues
    from .models import Admin, Secretary, Educator, Guardian, Student, SchoolClass, AttendanceRecord  # Updated Class to SchoolClass

    db.init_app(app)
