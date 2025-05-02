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
    def add_student(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Student")
        add_win.geometry("300x250")
        add_win.configure(bg="silver")

        tk.Label(add_win, text="Name:", bg="silver", fg="black").pack()
        name_entry = tk.Entry(add_win)
        name_entry.pack()

        tk.Label(add_win, text="Age:", bg="silver", fg="black").pack()
        age_entry = tk.Entry(add_win)
        age_entry.pack()

        tk.Label(add_win, text="Room Number:", bg="silver", fg="black").pack()
        room_entry = tk.Entry(add_win)
        room_entry.pack()
        def save_student():
            name = name_entry.get()
            age = age_entry.get()
            room = room_entry.get()

            if not name or not age or not room:
                messagebox.showerror("Input Error", "All fields are required!")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM rooms WHERE room_number = ?", (room,))
                existing_room = cursor.fetchone()
                if existing_room:
                    if existing_room[2] >= existing_room[1]:
                        raise sqlite3.IntegrityError("Room is full")
                    cursor.execute("UPDATE rooms SET occupied = occupied + 1 WHERE room_number = ?", (room,))
                else:
                    cursor.execute("INSERT INTO rooms (room_number, capacity, occupied) VALUES (?, ?, ?)",
                                   (room, 1, 1))

                cursor.execute("INSERT INTO students (name, age, room_number) VALUES (?, ?, ?)",
                               (name, int(age), room))

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Student added successfully!")
                add_win.destroy()
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Error", f"{e}")
            except ValueError:
                messagebox.showerror("Error", "Invalid age input.")
            except Exception as e:
                logging.error(f"Add Student Error: {e}")
                messagebox.showerror("Error", "An unexpected error occurred.")

        tk.Button(add_win, text="Save", command=save_student,
                  bg="silver", fg="black").pack(pady=10)
    def view_students(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("Student List")
        view_win.geometry("500x300")

        tree = ttk.Treeview(view_win, columns=("ID", "Name", "Age", "Room", "Fees Paid"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Age", text="Age")
        tree.heading("Room", text="Room")
        tree.heading("Fees Paid", text="Fees Paid")
        tree.pack(fill=tk.BOTH, expand=True)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            logging.error(f"View Students Error: {e}")
            messagebox.showerror("Error", "Failed to load students.")
