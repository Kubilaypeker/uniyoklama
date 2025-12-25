
import psycopg2
from flask import Flask

# Minimal config to match config.cfg
DB_URL = "postgresql://uniyoklama:uniyoklama@localhost:5432/uniyoklama"

try:
    conn = psycopg2.connect(DB_URL)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
