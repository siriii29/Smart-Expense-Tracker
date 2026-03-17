import sqlite3
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)  # Create data directory if it doesn't exist
DB_PATH = DATA_DIR / 'expenses.db'

def get_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Create categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Create expenses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )''')
        
        # Create default categories if they don't exist
        default_categories = [
            'Food & Dining', 'Shopping', 'Transportation', 'Housing', 
            'Entertainment', 'Healthcare', 'Education', 'Utilities', 'Others'
        ]
        
        for category in default_categories:
            try:
                cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            except sqlite3.IntegrityError:
                pass  # Category already exists
        
        conn.commit()

def add_expense(amount, category_name, payment_method, description, date):
    """Add a new expense to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Get or create category
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category = cursor.fetchone()
        
        if not category:
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            category_id = cursor.lastrowid
        else:
            category_id = category['id']
        
        # Insert expense
        cursor.execute('''
            INSERT INTO expenses (amount, category_id, payment_method, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (amount, category_id, payment_method, description, date))
        
        conn.commit()
        return cursor.lastrowid

def get_expenses(start_date=None, end_date=None, category=None):
    """Retrieve expenses with optional filters."""
    query = '''
        SELECT e.id, e.amount, c.name as category, e.payment_method, 
               e.description, e.date, e.created_at
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
    '''
    
    params = []
    conditions = []
    
    if start_date:
        conditions.append("e.date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("e.date <= ?")
        params.append(end_date)
    if category:
        conditions.append("c.name = ?")
        params.append(category)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY e.date DESC"
    
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params if params else None)
    
    return df

def get_categories():
    """Get all categories."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM categories ORDER BY name')
        return [row['name'] for row in cursor.fetchall()]

def add_category(name):
    """Add a new category."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def delete_expense(expense_id):
    """Delete an expense by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_expense_by_id(expense_id):
    """Get a single expense by its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, e.amount, c.name as category, e.payment_method, 
                   e.description, e.date
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.id = ?
        ''', (expense_id,))
        
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None

def update_expense(expense_id, amount, category_name, payment_method, description, date):
    """Update an existing expense."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Get or create category
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category = cursor.fetchone()
        
        if not category:
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            category_id = cursor.lastrowid
        else:
            category_id = category['id']
        
        # Update expense
        cursor.execute('''
            UPDATE expenses 
            SET amount = ?, 
                category_id = ?, 
                payment_method = ?, 
                description = ?, 
                date = ?
            WHERE id = ?
        ''', (amount, category_id, payment_method, description, date, expense_id))
        
        conn.commit()
        return cursor.rowcount > 0

def get_expense_summary():
    """Get summary statistics of expenses."""
    with get_connection() as conn:
        # Total expenses
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) as total FROM expenses')
        total = cursor.fetchone()['total'] or 0
        
        # Monthly spending
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, 
                   SUM(amount) as total
            FROM expenses
            GROUP BY month
            ORDER BY month DESC
            LIMIT 6
        ''')
        monthly = cursor.fetchall()
        
        # Top categories
        cursor.execute('''
            SELECT c.name as category, 
                   SUM(e.amount) as total
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            GROUP BY c.name
            ORDER BY total DESC
            LIMIT 5
        ''')
        top_categories = cursor.fetchall()
        
        return {
            'total_expenses': total,
            'monthly_spending': [dict(row) for row in monthly],
            'top_categories': [dict(row) for row in top_categories]
        }

def clear_all_data():
    """Delete all data from the database (expenses and categories)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses')
        cursor.execute('DELETE FROM categories')
        conn.commit()
        return True

# Initialize the database when this module is imported
init_db()
