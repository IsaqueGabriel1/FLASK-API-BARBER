from flask import Flask
import os
import sqlite3

app = Flask(__name__)

# Ensure "base" directory exists at project root and create SQLite DB
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
base_dir = os.path.join(project_root, 'base')
os.makedirs(base_dir, exist_ok=True)

# Database path: base\barbearia.db
db_path = os.path.join(base_dir, 'barbearia.db')

# Create DB and usuarios table if it doesn't exist
conn = sqlite3.connect(db_path)
try:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    nome TEXT,
                    email TEXT,
                    senha TEXT
                );''')
    conn.commit()
finally:
    conn.close()
