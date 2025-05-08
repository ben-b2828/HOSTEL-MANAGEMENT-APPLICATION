Hostel Management Application Documentation

 Introduction
Project Title: Hostel Management Application

Technologies Used: Python, Tkinter, SQLite
Purpose:
The Hostel Management Application is a desktop-based software developed using Python’s Tkinter for the GUI and SQLite for database management. The application simplifies and automates student hostel operations such as room assignment, fee collection, and student record management.

Application Objectives and Features
Objectives:
•	Maintain an up-to-date list of hostel residents.
•	Track room occupancy and availability.
•	Manage student fee payments.
•	Provide an intuitive graphical interface for hostel administrators.
Key Features:
•	Student registration with automatic room tracking.
•	Room capacity and occupancy management.
•	Real-time fee tracking and payment recording.
•	Student removal with cascading database updates.
•	Persistent data storage with SQLite.

Application Architecture
Architecture Overview:
1.	Frontend (GUI)
o	Built with Tkinter.
o	Consists of buttons and forms for user interaction.
2.	Backend (Database and Logic)
o	SQLite used for relational data storage.
o	Includes tables for students, rooms, and payments.
o	Foreign key constraints ensure referential integrity.
File Structure:
pgsql
CopyEdit
project/
├── hostel.py  (Main code)
├── .venv/
│   ├── Lib/
│   │   ├── hostel.db      (SQLite database)
│   │   └── error.log      (Log file)

Page 4: Database Design
Tables:
•	students
o	id: Primary key
o	name: Student's name
o	age: Integer
o	room_number: Foreign key (rooms.room_number)
o	fees_paid: Total amount paid
•	rooms
o	room_number: Primary key
o	capacity: Maximum occupancy
o	occupied: Currently occupied slots
•	payments
o	id: Primary key
o	student_id: Foreign key (students.id)
o	amount: Fee paid
o	date: Timestamp of transaction
Integrity Constraints:
•	Foreign key from payments.student_id to students.id
•	room_number in students references rooms

 Initialization and Logging
Database Initialization:
•	Runs on application startup via initialize_db()
•	Creates all necessary tables if they don’t already exist
Logging:
•	Errors are logged into error.log file
•	Uses logging module to track issues like database failures, unexpected exceptions
python
CopyEdit
logging.basicConfig(filename=".venv/Lib/error.log", level=logging.ERROR)

 GUI - Main Interface
Main Window:
•	Title: Hostel Management Application
•	Buttons:
o	Add Student
o	View Students
o	Manage Payments
o	Remove Student
o	Exit
Styling:
•	Background: Silver
•	Buttons: Grey or Red (for Exit)
•	Fonts: Arial, sizes adjusted for readability
python
CopyEdit
tk.Label(self.root, text="HostelApp", font=("Arial", 37))

Add Student Module
Functionality:
•	Opens a new window with fields for name, age, room
•	Checks if the room is full before assigning
•	Automatically creates a room entry if it doesn’t exist
Error Handling:
•	Empty fields prompt a messagebox
•	ValueError for age validation
•	SQLite errors logged and shown in GUI
Room Management:
•	Room capacity is assumed as 1 if it's newly created
•	Occupied count is updated accordingly

View & Remove Students
View Students:
•	Opens a Toplevel window with a Treeview widget
•	Displays ID, name, age, room, and fees paid
•	Queries data from students table
Remove Student:
•	Provides dropdown to select student
•	On removal:
o	Student is deleted
o	Room's occupied count is decremented
•	Includes checks for student existence

 Manage Payments
Payment Entry:
•	Dropdown of registered students
•	Entry field for amount
•	Records payment in payments table with timestamp
•	Updates fees_paid in students
Input Validation:
•	Ensures a student and amount are selected
•	Converts amount to float
•	Catches database exceptions
UX:
•	Clear field labeling
•	Success/failure message boxes guide the user

 Conclusion and Future Enhancements
Conclusion:
This application offers a functional and efficient way to manage student housing operations. By combining a simple GUI with persistent database storage, it bridges the gap between administrative needs and digital convenience.
Possible Improvements:
•	Add student photos or profile management
•	Search and filter functionalities
•	Dashboard with statistics (total students, full rooms)
•	Multi-room assignment or guest booking feature
•	Export data to Excel or PDF reports

