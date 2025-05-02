import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import logging
from datetime import datetime

# Enable foreign keys in SQLite


def connect_db():
    conn = sqlite3.connect(".venv/Lib/hostel.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Logging setup
logging.basicConfig(filename=".venv/Lib/error.log", level=logging.ERROR,
                    format="%(pastime)s - %(levelname)s - %(message)s")
