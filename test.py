# vulnerable_app.py
# ⚠️ Educational Use Only – Demonstrates common Python security flaws.

import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# === Insecure Database Setup ===
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

# === Vulnerability 1: Command Injection ===
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # ❌ Directly passing user input to os.system
    os.system(f"ping -c 1 {host}")
    return f"Pinging {host}..."

# === Vulnerability 2: SQL Injection ===
@app.route('/login')
def login():
    username = request.args.get('user')
    password = request.args.get('pass')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # ❌ Vulnerable to SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print("Executing:", query)
    c.execute(query)
    result = c.fetchall()
    conn.close()
    if result:
        return "Login successful!"
    else:
        return "Invalid credentials."

# === Vulnerability 3: Sensitive Data Exposure ===
@app.route('/debug')
def debug():
    # ❌ Exposes internal data
    return str(dict(request.args))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
