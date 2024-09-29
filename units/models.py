from . import db  # Import db from the package-level __init__.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, Date, ForeignKey, Integer, String
import datetime

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id: Mapped[int] = mapped_column(primary_key=True)
    admin_username: Mapped[str] = mapped_column(unique=True)
    admin_password: Mapped[str]
    admin_email: Mapped[str] = mapped_column(unique=True)

class Secretary(db.Model):
    __tablename__ = 'secretary'
    secretary_id: Mapped[int] = mapped_column(primary_key=True)
    secretary_username: Mapped[str] = mapped_column(unique=True)
    secretary_password: Mapped[str]
    secretary_first_name: Mapped[str]
    secretary_last_name: Mapped[str]
    secretary_email: Mapped[str] = mapped_column(unique=True)
    secretary_cell_number: Mapped[str] = mapped_column(unique=True)
    secretary_rsa_id_num: Mapped[str] = mapped_column(unique=True)

class Educator(db.Model):
    __tablename__ = 'educator'
    educator_id: Mapped[int] = mapped_column(primary_key=True)
    educator_username: Mapped[str] = mapped_column(unique=True)
    educator_password: Mapped[str]
    educator_first_name: Mapped[str]
    educator_last_name: Mapped[str]
    educator_email: Mapped[str] = mapped_column(unique=True)
    educator_cell_num: Mapped[str] = mapped_column(unique=True)
    educator_rsa_id_num: Mapped[str] = mapped_column(unique=True)

class Guardian(db.Model):
    __tablename__ = 'guardian'
    guardian_id: Mapped[int] = mapped_column(primary_key=True)
    guardian_username: Mapped[str] = mapped_column(unique=True)
    guardian_password: Mapped[str]
    guardian_first_name: Mapped[str]
    guardian_last_name: Mapped[str]
    guardian_email: Mapped[str] = mapped_column(unique=True)
    guardian_cell_number: Mapped[str] = mapped_column(unique=True)
    guardian_address: Mapped[str]
    guardian_rsa_id_number: Mapped[str] = mapped_column(unique=True)
    guardian_dependants_list: Mapped[dict] = mapped_column(JSON)

    dependants: Mapped[list["Student"]] = relationship(back_populates="guardian")

class Student(db.Model):
    __tablename__ = 'student'
    student_id: Mapped[int] = mapped_column(primary_key=True)
    student_first_name: Mapped[str]
    student_last_name: Mapped[str]
    student_rsa_id_number: Mapped[str] = mapped_column(unique=True)

    # Foreign key
    guardian_id: Mapped[int] = mapped_column(ForeignKey("guardian.guardian_id"))
    guardian: Mapped["Guardian"] = relationship(back_populates="dependants")

class SchoolClass(db.Model):  # Changed from Class to SchoolClass
    __tablename__ = 'class'
    class_id: Mapped[int] = mapped_column(primary_key=True)
    class_students: Mapped[dict] = mapped_column(JSON)

    # Foreign keys
    educator_id: Mapped[int] = mapped_column(ForeignKey("educator.educator_id"))

    attendance_record: Mapped[list["AttendanceRecord"]] = relationship(back_populates="class_")

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    attendance_record_id: Mapped[int] = mapped_column(primary_key=True)
    attendance_record_date: Mapped[datetime.date] = mapped_column(Date)
    attendance_record_list: Mapped[dict] = mapped_column(JSON)

    # Foreign key
    class_id: Mapped[int] = mapped_column(ForeignKey("class.class_id"))
    class_: Mapped["SchoolClass"] = relationship(back_populates="attendance_record")  # Updated the relationship

