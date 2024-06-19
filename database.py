import sqlite3

def init_db():
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 1000
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def get_balance(user_id):
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance

def update_balance(user_id, new_balance):
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
    conn.commit()
    conn.close()

def add_transaction(user_id, type, amount):
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (user_id, type, amount, date) VALUES (?, ?, ?, datetime("now"))', (user_id, type, amount))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('SELECT type, amount, date FROM transactions WHERE user_id = ?', (user_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions
