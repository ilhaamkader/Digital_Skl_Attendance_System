from units.student_attendance_tracker import MissingStudentIdentifier

class MissingStudentReport:
    def __init__(self, class_register_dict=None):
        """Initializes with an optional class register dictionary."""
        self.class_register_dict = class_register_dict or {}
        self.class_missing_children = {}

    def set_class_register_dict(self, class_register_dict):
        """Sets the class register dictionary."""
        self.class_register_dict = class_register_dict

    def compile_missing_students(self):
        """Compile the missing students report."""
        for class_key, student_list in self.class_register_dict.items():
            missing_students = MissingStudentIdentifier(student_list).get_missing_students()
            if missing_students:
                self.class_missing_children[class_key] = missing_students

    def get_missing_student_class_list(self):
        """Returns the compiled missing students by class."""
        self.compile_missing_students()
        return self.class_missing_children if self.class_missing_children else None
