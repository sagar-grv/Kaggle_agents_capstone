"""
BankDatabase - Mock Banking System
===================================

Provides a SQLite-based mock database for customer data simulation.
This replaces the need for actual bank system integration during development and demo.

Database Schema:
----------------
customers table:
  - email (TEXT, PRIMARY KEY): Customer email address
  - name (TEXT): Full customer name
  - account_balance (REAL): Current account balance
  - card_status (TEXT): 'ACTIVE' or 'BLOCKED'
  - risk_score (INTEGER): Security risk score (1-10)

transactions table:
  - id (INTEGER PRIMARY KEY)
  - customer_email (TEXT): Foreign key to customers
  - amount (REAL): Transaction amount
  - description (TEXT): Transaction description
  - timestamp (TEXT): Transaction datetime

Pre-seeded Customers:
---------------------
- alice@example.com: Balance $12,450.50
- bob@example.com: Balance $3,201.75
- charlie@example.com: Balance $98,200.00

Available Methods:
------------------
- get_customer_by_email(email): Retrieve customer record
- get_balance(email): Get account balance
- get_recent_transactions(email, limit=5): Get transaction history
- get_card_status(email): Check if card is ACTIVE/BLOCKED
- block_card(email): Block customer's card for security
- close(): Properly close database connection

Author: BankAssist Team
"""

import sqlite3
import random
from datetime import datetime, timedelta

class BankDatabase:
    def __init__(self, db_name="bankassist.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._seed_data()

    def _create_tables(self):
        # Customers Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                risk_score INTEGER
            )
        ''')
        
        # Accounts Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                customer_id TEXT,
                account_type TEXT,
                balance REAL,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        ''')

        # Transactions Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                account_id TEXT,
                date TEXT,
                amount REAL,
                merchant TEXT,
                category TEXT,
                FOREIGN KEY(account_id) REFERENCES accounts(account_id)
            )
        ''')
        
        # Migration: Add category column if it doesn't exist (for existing databases)
        try:
            self.cursor.execute("SELECT category FROM transactions LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("ALTER TABLE transactions ADD COLUMN category TEXT")
            self.conn.commit()

        # Cards Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                card_id TEXT PRIMARY KEY,
                customer_id TEXT,
                status TEXT, -- 'ACTIVE', 'BLOCKED'
                limit_amount REAL,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        ''')

        # Audit Logs Table (Global Monitoring)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_email TEXT,
                query TEXT,
                agent_used TEXT,
                response TEXT,
                feedback TEXT
            )
        ''')
        self.conn.commit()

    def log_event(self, user_email, query, agent_used, response, feedback=None):
        """Log a system event for audit purposes."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO audit_logs (timestamp, user_email, query, agent_used, response, feedback)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, user_email, query, agent_used, response, feedback))
        self.conn.commit()

    def get_all_logs(self):
        """Retrieve all audit logs for admin dashboard."""
        self.cursor.execute('SELECT * FROM audit_logs ORDER BY timestamp DESC')
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def _seed_data(self):
        print("Seeding mock data...")
        
        # Mock Customers
        customers = [
            ("CUST001", "Alice Johnson", "alice@example.com", "555-0101", 10),
            ("CUST002", "Bob Smith", "bob@example.com", "555-0102", 80), # High risk
            ("CUST003", "Charlie Brown", "charlie@example.com", "555-0103", 5)
        ]
        self.cursor.executemany("INSERT OR IGNORE INTO customers VALUES (?,?,?,?,?)", customers)

        # Mock Accounts
        accounts = [
            ("ACC001", "CUST001", "Checking", 5400.50),
            ("ACC002", "CUST001", "Savings", 12000.00),
            ("ACC003", "CUST002", "Checking", 200.00),
            ("ACC004", "CUST003", "Checking", 850.00)
        ]
        self.cursor.executemany("INSERT OR IGNORE INTO accounts VALUES (?,?,?,?)", accounts)

        # Mock Cards
        cards = [
            ("CARD001", "CUST001", "ACTIVE", 5000),
            ("CARD002", "CUST002", "BLOCKED", 1000),
            ("CARD003", "CUST003", "ACTIVE", 2000)
        ]
        self.cursor.executemany("INSERT OR IGNORE INTO cards VALUES (?,?,?,?)", cards)

        # Mock Transactions
        transactions = []
        for acc_id in ["ACC001", "ACC002", "ACC003"]:
            for i in range(5):
                t_id = f"TXN{random.randint(1000,9999)}"
                date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
                amt = round(random.uniform(-500, 500), 2)
                merch = random.choice(["Amazon", "Uber", "Walmart", "Netflix", "Salary"])
                cat = "Shopping" if amt < 0 else "Income"
                transactions.append((t_id, acc_id, date, amt, merch, cat))
        
        self.cursor.executemany("INSERT OR IGNORE INTO transactions VALUES (?,?,?,?,?,?)", transactions)
        self.conn.commit()

    # --- Tools for Agents ---
    def get_customer_by_email(self, email):
        self.cursor.execute("SELECT * FROM customers WHERE email=?", (email,))
        return self.cursor.fetchone()

    def get_balance(self, customer_id):
        self.cursor.execute("SELECT account_type, balance FROM accounts WHERE customer_id=?", (customer_id,))
        return self.cursor.fetchall()

    def get_recent_transactions(self, customer_id, limit=5):
        self.cursor.execute('''
            SELECT t.date, t.merchant, t.amount 
            FROM transactions t 
            JOIN accounts a ON t.account_id = a.account_id 
            WHERE a.customer_id=? 
            ORDER BY t.date DESC LIMIT ?
        ''', (customer_id, limit))
        return self.cursor.fetchall()

    def block_card(self, customer_id):
        self.cursor.execute("UPDATE cards SET status='BLOCKED' WHERE customer_id=?", (customer_id,))
        self.conn.commit()
        return "Card blocked successfully."

    def get_card_status(self, customer_id):
        self.cursor.execute("SELECT card_id, status FROM cards WHERE customer_id=?", (customer_id,))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
