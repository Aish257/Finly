import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "finly.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for Expenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            notes TEXT
        )
    """)
    
    # Table for Financial Goals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_savings REAL NOT NULL,
            target_date TEXT NOT NULL
        )
    """)
    
    conn.commit()
    
    # Insert initial sample seed data if user has no expenses
    cursor.execute("SELECT COUNT(*) as count FROM expenses")
    if cursor.fetchone()['count'] == 0:
        seed_data = [
            ("demo@finly.app", "Grocery Store", 1850.0, "Food", "2026-08-10", "Weekly provisions"),
            ("demo@finly.app", "Metro Pass", 600.0, "Transport", "2026-08-12", "Monthly train pass"),
            ("demo@finly.app", "Python & Finance Course", 1200.0, "Education", "2026-08-14", "Udemy online course"),
            ("demo@finly.app", "Electricity Bill", 1450.0, "Bills", "2026-08-15", "Utility bill"),
            ("demo@finly.app", "Movie Night & Snacks", 750.0, "Entertainment", "2026-08-18", "Weekend outing"),
            ("demo@finly.app", "New Headphones", 2499.0, "Shopping", "2026-08-20", "Tech gadgets")
        ]
        cursor.executemany("""
            INSERT INTO expenses (user_id, title, amount, category, date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, seed_data)
        
        seed_goals = [
            ("demo@finly.app", "Emergency Fund", 50000.0, 22000.0, "2026-12-31"),
            ("demo@finly.app", "First Stock Investment Portfolio", 25000.0, 10000.0, "2026-10-15")
        ]
        cursor.executemany("""
            INSERT INTO goals (user_id, goal_name, target_amount, current_savings, target_date)
            VALUES (?, ?, ?, ?, ?)
        """, seed_goals)
        conn.commit()

    conn.close()

# Expenses CRUD
def add_expense(user_id, title, amount, category, date_str, notes=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (user_id, title, amount, category, date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, amount, category, date_str, notes))
    conn.commit()
    conn.close()

def get_expenses(user_id):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC", conn, params=(user_id,))
    conn.close()
    return df

def update_expense(expense_id, title, amount, category, date_str, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET title = ?, amount = ?, category = ?, date = ?, notes = ?
        WHERE id = ?
    """, (title, amount, category, date_str, notes, expense_id))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# Goals CRUD
def add_goal(user_id, goal_name, target_amount, current_savings, target_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (user_id, goal_name, target_amount, current_savings, target_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, goal_name, target_amount, current_savings, target_date))
    conn.commit()
    conn.close()

def get_goals(user_id):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM goals WHERE user_id = ? ORDER BY id DESC", conn, params=(user_id,))
    conn.close()
    return df

def update_goal(goal_id, goal_name, target_amount, current_savings, target_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE goals
        SET goal_name = ?, target_amount = ?, current_savings = ?, target_date = ?
        WHERE id = ?
    """, (goal_name, target_amount, current_savings, target_date, goal_id))
    conn.commit()
    conn.close()

def delete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()
