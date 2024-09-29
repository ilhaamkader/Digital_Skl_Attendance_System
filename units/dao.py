from .models import Admin, db # Secretary, Educator, Division, Grade, Guardian, Student, Class, AttendanceRecord

class AdminDAO:
    @staticmethod
    def get_all_admins():
        return Admin.query.all()

    @staticmethod
    def get_admin_by_id(admin_id):
        return Admin.query.get(admin_id)

    @staticmethod
    def add_admin(username, password, email):
        new_admin = Admin(admin_username=username, admin_password=password, admin_email=email)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin added:", new_admin)  # Debug output

    @staticmethod
    def delete_admin(admin_id):
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
'''
class SecretaryDAO:
    @staticmethod
    def get_all_secretaries():
        return Secretary.query.all()

    @staticmethod
    def get_secretary_by_id(secretary_id):
        return Secretary.query.get(secretary_id)

    @staticmethod
    def add_secretary(username, password, first_name, last_name, email, cell_number, rsa_id_num):
        new_secretary = Secretary(
            secretary_username=username,
            secretary_password=password,
            secretary_first_name=first_name,
            secretary_last_name=last_name,
            secretary_email=email,
            secretary_cell_number=cell_number,
            secretary_rsa_id_num=rsa_id_num
        )
        db.session.add(new_secretary)
        db.session.commit()

    @staticmethod
    def delete_secretary(secretary_id):
        secretary = Secretary.query.get(secretary_id)
        if secretary:
            db.session.delete(secretary)
            db.session.commit()

class EducatorDAO:
    @staticmethod
    def get_all_educators():
        return Educator.query.all()

    @staticmethod
    def get_educator_by_id(educator_id):
        return Educator.query.get(educator_id)

    @staticmethod
    def add_educator(username, password, first_name, last_name, email, cell_num, rsa_id_num):
        new_educator = Educator(
            educator_username=username,
            educator_password=password,
            educator_first_name=first_name,
            educator_last_name=last_name,
            educator_email=email,
            educator_cell_num=cell_num,
            educator_rsa_id_num=rsa_id_num
        )
        db.session.add(new_educator)
        db.session.commit()

    @staticmethod
    def delete_educator(educator_id):
        educator = Educator.query.get(educator_id)
        if educator:
            db.session.delete(educator)
            db.session.commit()

class DivisionDAO:
    @staticmethod
    def get_all_divisions():
        return Division.query.all()

    @staticmethod
    def get_division_by_id(division_id):
        return Division.query.get(division_id)

    @staticmethod
    def add_division(division_name):
        new_division = Division(division_name=division_name)
        db.session.add(new_division)
        db.session.commit()

    @staticmethod
    def delete_division(division_id):
        division = Division.query.get(division_id)
        if division:
            db.session.delete(division)
            db.session.commit()

class GradeDAO:
    @staticmethod
    def get_all_grades():
        return Grade.query.all()

    @staticmethod
    def get_grade_by_id(grade_id):
        return Grade.query.get(grade_id)

    @staticmethod
    def add_grade(grade_number):
        new_grade = Grade(grade_number=grade_number)
        db.session.add(new_grade)
        db.session.commit()

    @staticmethod
    def delete_grade(grade_id):
        grade = Grade.query.get(grade_id)
        if grade:
            db.session.delete(grade)
            db.session.commit()

class GuardianDAO:
    @staticmethod
    def get_all_guardians():
        return Guardian.query.all()

    @staticmethod
    def get_guardian_by_id(guardian_id):
        return Guardian.query.get(guardian_id)

    @staticmethod
    def add_guardian(username, password, first_name, last_name, email, cell_number, address, rsa_id_number, dependants_list):
        new_guardian = Guardian(
            guardian_username=username,
            guardian_password=password,
            guardian_first_name=first_name,
            guardian_last_name=last_name,
            guardian_email=email,
            guardian_cell_number=cell_number,
            guardian_address=address,
            guardian_rsa_id_number=rsa_id_number,
            guardian_dependants_list=dependants_list
        )
        db.session.add(new_guardian)
        db.session.commit()

    @staticmethod
    def delete_guardian(guardian_id):
        guardian = Guardian.query.get(guardian_id)
        if guardian:
            db.session.delete(guardian)
            db.session.commit()

class StudentDAO:
    @staticmethod
    def get_all_students():
        return Student.query.all()

    @staticmethod
    def get_student_by_id(student_id):
        return Student.query.get(student_id)

    @staticmethod
    def add_student(first_name, last_name, rsa_id_number, guardian_id):
        new_student = Student(
            student_first_name=first_name,
            student_last_name=last_name,
            student_rsa_id_number=rsa_id_number,
            guardian_id=guardian_id
        )
        db.session.add(new_student)
        db.session.commit()

    @staticmethod
    def delete_student(student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()

class ClassDAO:
    @staticmethod
    def get_all_classes():
        return Class.query.all()

    @staticmethod
    def get_class_by_id(class_id):
        return Class.query.get(class_id)

    @staticmethod
    def add_class(grade_id, division_id, educator_id, class_students):
        new_class = Class(
            grade_id=grade_id,
            division_id=division_id,
            educator_id=educator_id,
            class_students=class_students
        )
        db.session.add(new_class)
        db.session.commit()

    @staticmethod
    def delete_class(class_id):
        class_ = Class.query.get(class_id)
        if class_:
            db.session.delete(class_)
            db.session.commit()

class AttendanceRecordDAO:
    @staticmethod
    def get_all_attendance_records():
        return AttendanceRecord.query.all()

    @staticmethod
    def get_attendance_record_by_id(attendance_record_id):
        return AttendanceRecord.query.get(attendance_record_id)

    @staticmethod
    def add_attendance_record(attendance_record_date, attendance_record_list, class_id):
        new_record = AttendanceRecord(
            attendance_record_date=attendance_record_date,
            attendance_record_list=attendance_record_list,
            class_id=class_id
        )
        db.session.add(new_record)
        db.session.commit()

    @staticmethod
    def delete_attendance_record(attendance_record_id):
        record = AttendanceRecord.query.get(attendance_record_id)
        if record:
            db.session.delete(record)
            db.session.commit()

            
'''