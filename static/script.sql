-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS attendance_record;
DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS guardian;
DROP TABLE IF EXISTS educator;
DROP TABLE IF EXISTS secretary;
DROP TABLE IF EXISTS admin;

-- Create tables

CREATE TABLE admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_username VARCHAR(255) UNIQUE NOT NULL,
    admin_password VARCHAR(255) NOT NULL,
    admin_email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE secretary (
    secretary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    secretary_username VARCHAR(255) UNIQUE NOT NULL,
    secretary_password VARCHAR(255) NOT NULL,
    secretary_first_name VARCHAR(255) NOT NULL,
    secretary_last_name VARCHAR(255) NOT NULL,
    secretary_email VARCHAR(255) UNIQUE NOT NULL,
    secretary_cell_number VARCHAR(20) UNIQUE NOT NULL,
    secretary_rsa_id_num VARCHAR(13) UNIQUE NOT NULL
);

CREATE TABLE educator (
    educator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    educator_username VARCHAR(255) UNIQUE NOT NULL,
    educator_password VARCHAR(255) NOT NULL,
    educator_first_name VARCHAR(255) NOT NULL,
    educator_last_name VARCHAR(255) NOT NULL,
    educator_email VARCHAR(255) UNIQUE NOT NULL,
    educator_cell_num VARCHAR(20) UNIQUE NOT NULL,
    educator_rsa_id_num VARCHAR(13) UNIQUE NOT NULL
);

CREATE TABLE guardian (
    guardian_id INTEGER PRIMARY KEY AUTOINCREMENT,
    guardian_username VARCHAR(255) UNIQUE NOT NULL,
    guardian_password VARCHAR(255) NOT NULL,
    guardian_first_name VARCHAR(255) NOT NULL,
    guardian_last_name VARCHAR(255) NOT NULL,
    guardian_email VARCHAR(255) UNIQUE NOT NULL,
    guardian_cell_number VARCHAR(20) UNIQUE NOT NULL,
    guardian_address VARCHAR(255) NOT NULL,
    guardian_rsa_id_number VARCHAR(13) UNIQUE NOT NULL,
    guardian_dependants_list JSON NOT NULL
);

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_first_name VARCHAR(255) NOT NULL,
    student_last_name VARCHAR(255) NOT NULL,
    student_rsa_id_number VARCHAR(13) UNIQUE NOT NULL,
    guardian_id INTEGER NOT NULL REFERENCES guardian(guardian_id)
);

CREATE TABLE class (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_students JSON NOT NULL,
    educator_id INTEGER NOT NULL REFERENCES educator(educator_id)
);

CREATE TABLE attendance_record (
    attendance_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    attendance_record_date DATE NOT NULL,
    attendance_record_list JSON NOT NULL,
    class_id INTEGER NOT NULL REFERENCES class(class_id)
);

-- Insert data into tables

-- Admins
INSERT INTO admin (admin_username, admin_password, admin_email)
VALUES 
('admin_1', 'password123', 'admin1@example.com'),
('admin_2', 'password456', 'admin2@example.com');

-- Secretaries
INSERT INTO secretary (secretary_username, secretary_password, secretary_first_name, secretary_last_name, secretary_email, secretary_cell_number, secretary_rsa_id_num)
VALUES 
('sec_jane', 'password123', 'Jane', 'Doe', 'jane.doe@example.com', '0712345678', '9001011234567'),
('sec_mark', 'password456', 'Mark', 'Smith', 'mark.smith@example.com', '0723456789', '8902022345678');

-- Educators
INSERT INTO educator (educator_username, educator_password, educator_first_name, educator_last_name, educator_email, educator_cell_num, educator_rsa_id_num)
VALUES 
('educator_john', 'teachpass123', 'John', 'Doe', 'john.doe@example.com', '0812345678', '8303033456789'),
('educator_susan', 'teachpass456', 'Susan', 'Parker', 'susan.parker@example.com', '0823456789', '8504044567890');

-- Guardians
INSERT INTO guardian (guardian_username, guardian_password, guardian_first_name, guardian_last_name, guardian_email, guardian_cell_number, guardian_address, guardian_rsa_id_number, guardian_dependants_list)
VALUES 
('guardian_mike', 'mypassword1', 'Michael', 'Johnson', 'michael.johnson@example.com', '0734567890', '123 Oak Street', '7805055678901', '{"dependants": ["student_1"]}'),
('guardian_linda', 'mypassword2', 'Linda', 'Williams', 'linda.williams@example.com', '0745678901', '456 Pine Avenue', '7706066789012', '{"dependants": ["student_2", "student_3"]}');

-- Students
INSERT INTO student (student_first_name, student_last_name, student_rsa_id_number, guardian_id)
VALUES 
('Jake', 'Johnson', '0501013456789', 1),
('Emily', 'Williams', '0802022345678', 2),
('Sam', 'Williams', '1003031234567', 2);

-- Classes
INSERT INTO class (class_students, educator_id)
VALUES 
('{"students": ["student_1", "student_2"]}', 1),
('{"students": ["student_3"]}', 2);

-- Attendance Records
INSERT INTO attendance_record (attendance_record_date, attendance_record_list, class_id)
VALUES 
('2024-09-25', '{"present": ["student_1"], "absent": ["student_2"]}', 1),
('2024-09-26', '{"present": ["student_3"]}', 2),
('2024-09-27', '{"present": ["student_1", "student_2"]}', 1);
