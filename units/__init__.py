from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app):
    # Import models only after app is initialized to avoid circular import issues
    from .models import Admin, Secretary, Educator, Guardian, Student, SchoolClass, AttendanceRecord

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Specify login route for unauthorized access

    @login_manager.user_loader
    def load_user(user_id):
        from .models import Admin, Secretary, Educator, Guardian
        # Load user from the database by ID (search all user types)
        return Admin.query.get(int(user_id)) or \
               Secretary.query.get(int(user_id)) or \
               Educator.query.get(int(user_id)) or \
               Guardian.query.get(int(user_id))
