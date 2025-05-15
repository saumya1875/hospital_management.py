-- Create the database
CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;
drop database hospital_management;
-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Create the doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255) NOT NULL
);
DROP TABLE IF EXISTS patients, doctors, users;

-- Create the patients table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    doctor_id INT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
drop tables doctors;
DROP TABLE IF EXISTS doctors;

-- Sample data insertion
select * from patients;
-- Inserting users
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('doctor', 'doctor123', 'doctor'),
('receptionist', 'receptionist123', 'receptionist');
select * from doctors;
-- Inserting doctors
INSERT INTO doctors (name, specialty) VALUES
('Dr. Prashant', 'Cardiologist'),
('Dr. Dinesh', 'Neurologist'),
('Dr. Purnima', 'Pediatrician');

-- Inserting patients
INSERT INTO patients (name, age, gender, address, doctor_id) VALUES
('Deepika', 30, 'Female', '123 Main St', 1),
('Rahul', 45, 'Male', '456 Oak St', 2),
('Aviral', 60, 'Male', '789 Pine St', 3);
SELECT id, name, age, gender FROM patients;
SELECT p.id AS patient_id, p.name AS patient_name, p.age, p.gender, d.name AS doctor_name
FROM patients p
INNER JOIN doctors d ON p.doctor_id = d.id;

select *from patients;
