import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(num_contacts):
        name = f'Cody Stidham {i}'
        phone = f'stidhalt@miamioh.edu{i}'
        db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(20)  # Generate 20 test contacts.
