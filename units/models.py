from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer,String
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

class Admin(db.Model):
    admin_id:Mapped[int] = mapped_column(primary_key=True)
    admin_username:Mapped[str] = mapped_column(unique=True)
    admin_password:Mapped[str]
    admin_email:Mapped[str] = mapped_column(unique=True)

class Secretary(db.Model):
    secretary_id:Mapped[int] = mapped_column(primary_key=True)
    secretary_username:Mapped[str] = mapped_column(unique=True)
    secretary_password:Mapped[str]
    secretary_first_name:Mapped[str]
    secretary_last_name:Mapped[str]
    secretary_email:Mapped[str] = mapped_column(unique=True)
    secretary_cell_number:Mapped[str] = mapped_column(unique=True)
    secretary_rsa_id_num:Mapped[str] = mapped_column(unique=True)
    
    
    
class Educator(db.Model):
    educator_id:Mapped[int] = mapped_column(primary_key=True)
    educator_username:Mapped[str] = mapped_column(unique=True)
    educator_password:Mapped[str]
    educator_first_name:Mapped[str]
    educator_last_name:Mapped[str]
    educator_email:Mapped[str] = mapped_column(unique=True)
    educator_cell_num:Mapped[str] = mapped_column(unique=True)
    educator_rsa_id_num:Mapped[str] = mapped_column(unique=True)

class Division(db.Model):
    division_id:Mapped[str] = mapped_column(primary_key=True)
    division_name:Mapped[str] = mapped_column(unique=True)

class Grade(db.Model):
    grade_id:Mapped[int] = mapped_column(primary_key=True)
    grade_number:Mapped[str] = mapped_column(unique=True)

class Guardian(db.Model):
    guardian_id:Mapped[int] = mapped_column(primary_key=True)
    guardian_username:Mapped[str] = mapped_column(unique=True)
    guardian_password:Mapped[str]
    guardian_first_name:Mapped[str]
    guardian_last_name:Mapped[str]
    guardian_email:Mapped[str] = mapped_column(unique=True)
    guardian_cell_number:Mapped[str] = mapped_column(unique=True)
    guardian_address:Mapped[str]
    guardian_rsa_id_number:Mapped[str] = mapped_column(unique=True)
    guardian_dependants_list

class Student(db.Model):
    student_id:Mapped[int] = mapped_column(primary_key=True)
    student_first_name:Mapped[str]
    student_last_name:Mapped[str]
    student_rsa_id_number:Mapped[str] = mapped_column(unique=True)
    
    #Foreign key
    guardian_id

class Class(db.Model):
    class_id:Mapped[int] = mapped_column(primary_key=True)
    class_students
    
    #Foreign keys
    grade_id
    division_id
    educator_id

class AttendenceRecord(db.Model):
    attendence_record_id
    attendence_record_date
    attendence_record_list
    
    #Foreign key
    class_id
    

with app.app_context():
    db.create_all()