from . import db  # Import db from the package-level __init__.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, Date, ForeignKey, Integer, String
import datetime
from flask_login import UserMixin  # Added UserMixin for Flask-Login

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    admin_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    def get_id(self):
        return str(self.admin_id)

class Secretary(db.Model, UserMixin):
    __tablename__ = 'secretary'
    secretary_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    cell_number: Mapped[str] = mapped_column(unique=True)
    rsa_id_num: Mapped[str] = mapped_column(unique=True)

    def get_id(self):
        return str(self.secretary_id)

class Educator(db.Model, UserMixin):
    __tablename__ = 'educator'
    educator_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    cell_number: Mapped[str] = mapped_column(unique=True)
    rsa_id_num: Mapped[str] = mapped_column(unique=True)

    def get_id(self):
        return str(self.educator_id)

class Guardian(db.Model, UserMixin):
    __tablename__ = 'guardian'
    guardian_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    cell_number: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    rsa_id_number: Mapped[str] = mapped_column(unique=True)
    guardian_dependants_list: Mapped[list] = mapped_column(JSON) # changed dict to list

    dependants: Mapped[list["Student"]] = relationship(back_populates="guardian")

class Student(db.Model):
    __tablename__ = 'student'
    student_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    rsa_id_number: Mapped[str] = mapped_column(unique=True)

    # Foreign key
    guardian_id: Mapped[int] = mapped_column(ForeignKey("guardian.guardian_id"))
    guardian: Mapped["Guardian"] = relationship(back_populates="dependants")

class SchoolClass(db.Model):  # Changed from Class to SchoolClass
    __tablename__ = 'class'
    class_id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    division: Mapped[str] = mapped_column(String(1), nullable=False)  
    class_students: Mapped[list] = mapped_column(JSON) # changed dict to list

    # Foreign keys
    educator_id: Mapped[int] = mapped_column(ForeignKey("educator.educator_id"))

    attendance_record: Mapped[list["AttendanceRecord"]] = relationship(back_populates="class_")

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    attendance_record_id: Mapped[int] = mapped_column(primary_key=True)
    attendance_record_date: Mapped[datetime.date] = mapped_column(Date)
    attendance_record_list: Mapped[list] = mapped_column(JSON) # changed dict to list

    # Foreign key
    class_id: Mapped[int] = mapped_column(ForeignKey("class.class_id"))
    class_: Mapped["SchoolClass"] = relationship(back_populates="attendance_record")  # Updated the relationship

