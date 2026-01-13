import mysql.connector
import hashlib

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9087",
    database="medicaps_expense"
)

cursor = conn.cursor()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
