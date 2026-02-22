# Patient Tracking and Management System

## Overview
A web-based hospital management system developed for Programming Laboratory II (Project 3).  
The application enables patients to register and manage appointments, doctors to view and manage patients/appointments, and administrators to manage system entities.

## Core Features
- Role-based login (Patient / Doctor / Admin)
- Appointment management (create, update, cancel)
- Medical report management:
  - Upload and store report files in a file storage system
  - Store file URLs in the database
  - Store medical report data also in JSON format
- Database design with relational tables and normalization
- Triggers to keep related tables consistent after insert/delete operations
- Dynamic UI updates using AJAX (upload/download without full page refresh)
- Notification system for new/updated medical reports
- Search queries from the UI (patients, doctors, appointments, reports)

## Database
Main entities include Patients, Doctors, Admin, Appointments, and Medical Reports.  
An ER diagram and schema-related materials are provided under `database/`.

## Security
- Secure communication (HTTPS)
- Password handling and data protection measures

## Documentation
- Final report (IEEE): `Project_Report.pdf`
