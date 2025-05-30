from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contact WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Contact deleted successfully.'
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            if name and email:
                db = get_db()
                db.execute('INSERT INTO contact (name, email) VALUES (?, ?)', (name, email))
                db.commit()
                message = 'Contact added successfully.'
            else:
                message = 'Missing name or email.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM contact').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <body style="background-color:#36f7ba;">
        <head>
            <title>CIT225 Final Project!</title>
        </head>
        <body>
            <h2>Add Emails!</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="email">Email:</label><br>
                <input type="text" id="email" name="email" required><br><br>

                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if contacts %}
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Delete</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr>
                            <td>{{ contact['name'] }}</td>
                            <td>{{ contact['email'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
