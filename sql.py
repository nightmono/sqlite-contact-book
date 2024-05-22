import sqlite3

connection = sqlite3.connect("contact-book.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT,
        phone_number TEXT,
        notes TEXT
    )
""")

connection.commit()

def get_contacts() -> tuple:
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    return contacts

def add_contact(first_name, last_name="", phone_number="", notes=""):
    cursor.execute("""
        INSERT INTO contacts (first_name, last_name, phone_number, notes)
        VALUES (?, ?, ?, ?)
    """, (first_name, last_name, phone_number, notes))

    connection.commit()