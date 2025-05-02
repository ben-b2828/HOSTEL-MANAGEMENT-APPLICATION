import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import logging
from datetime import datetime




def connect_db():
    conn = sqlite3.connect(".venv/Lib/hostel.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Logging setup
logging.basicConfig(filename=".venv/Lib/error.log", level=logging.ERROR,
                    format="%(pastime)s - %(levelname)s - %(message)s")

def initialize_db():
    try:
        conn = connect_db()
        cursor = conn.cursor()


        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER,
                            room_number TEXT UNIQUE,
                            fees_paid REAL DEFAULT 0.0
                        )''')
 cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                            room_number TEXT PRIMARY KEY,
                            capacity INTEGER,
                            occupied INTEGER DEFAULT 0
                        )''')


        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_id INTEGER,
                            amount REAL,
                            date TEXT,
                            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
                        )''')

        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Database Initialization Error: {e}")
        messagebox.showerror("Database Error", "Failed to initialize the database.")


class HostelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management App")
        self.root.geometry("600x400")
        self.root.configure(bg="silver")

        self.setup_ui()
    def setup_ui(self):
        tk.Label(self.root, text="HostelApp", font=("Arial", 37),
                 bg="gold", fg="black").pack(pady=10)

        tk.Button(self.root, text="Add Student", command=self.add_student,
                  bg="grey", fg="black").pack(pady=12)
        tk.Button(self.root, text="View Students", command=self.view_students,
                  bg="grey", fg="black").pack(pady=12)
        tk.Button(self.root, text="Manage Payments", command=self.manage_payments,
                  bg="grey", fg="black").pack(pady=12)
        tk.Button(self.root, text="Remove Student", command=self.remove_student,
                  bg="grey", fg="black").pack(pady=12)
        tk.Button(self.root, text="Exit", command=self.root.quit,
                  bg="red", fg="black").pack(pady=12)
