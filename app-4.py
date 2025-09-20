# app.py
# WARNING: This Flask app demonstrates both VULNERABLE and SECURE code for SQL Injection and XSS for educational purposes.
# Do NOT use in production or on a public server. Run it locally for training only.

from flask import Flask, request, render_template_string
import sqlite3
import logging
from markupsafe import escape

# Setup logging to diagnose issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Function to get database connection
def get_db():
    conn = sqlite3.connect('sqlitedb.db')
    conn.row_factory = sqlite3.Row  # To return rows as dicts
    return conn

# Initialize the database
with get_db() as db:
    db.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')
    db.commit()

# Health check endpoint for debugging
@app.route('/health', methods=['GET'])
def health():
    logger.info("Health check accessed")
    return "Flask app is running", 200

# Home route: Display all notes and forms
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    db.close()

    # Enhanced HTML template with modern styling
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Notes Taking App</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }
            .section {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .vulnerable {
                border-left: 5px solid #ff4444;
            }
            .secure {
                border-left: 5px solid #4CAF50;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .form-group input, .form-group textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }
            .form-group textarea {
                height: 100px;
                resize: vertical;
            }
            .form-group button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .form-group button:hover {
                background-color: #45a049;
            }
            .notes-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }
            .note-card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: 300px;
            }
            .note-card.vulnerable {
                border-left: 5px solid #ff4444;
            }
            .note-card.secure {
                border-left: 5px solid #4CAF50;
            }
            .note-card h4 {
                margin: 0 0 10px;
                font-size: 18px;
                color: #333;
            }
            .note-card p {
                margin: 0 0 10px;
                color: #555;
            }
            .note-card button {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .note-card button:hover {
                background-color: #cc0000;
            }
            .error {
                color: #ff4444;
                font-weight: bold;
                padding: 10px;
                background-color: #ffe6e6;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .success {
                color: #4CAF50;
                font-weight: bold;
                padding: 10px;
                background-color: #e6ffe6;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .row {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }
            .column {
                flex: 1;
                min-width: 300px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Simple Notes Taking App</h1>
            <p style="text-align: center; color: #555;">
                Explore SQL Injection and XSS vulnerabilities in a controlled environment. Use the forms below to add, search, or delete notes, comparing vulnerable and secure implementations.
            </p>
            
            <div class="row">
                <div class="column">
                    <div class="section vulnerable">
                        <h2>Vulnerable Add Note (SQLi Risk)</h2>
                        <form action="/add_vulnerable" method="POST">
                            <div class="form-group">
                                <label for="vuln-title">Title</label>
                                <input type="text" id="vuln-title" name="title" placeholder="Enter note title" required>
                            </div>
                            <div class="form-group">
                                <label for="vuln-content">Content</label>
                                <textarea id="vuln-content" name="content" placeholder="Enter note content" required></textarea>
                            </div>
                            <div class="form-group">
                                <button type="submit">Add Note (Vulnerable)</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="column">
                    <div class="section secure">
                        <h2>Secure Add Note</h2>
                        <form action="/add_secure" method="POST">
                            <div class="form-group">
                                <label for="secure-title">Title</label>
                                <input type="text" id="secure-title" name="title" placeholder="Enter note title" required>
                            </div>
                            <div class="form-group">
                                <label for="secure-content">Content</label>
                                <textarea id="secure-content" name="content" placeholder="Enter note content" required></textarea>
                            </div>
                            <div class="form-group">
                                <button type="submit">Add Note (Secure)</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Existing Notes</h2>
                <div class="row">
                    <div class="column">
                        <h3>Vulnerable Display (XSS Risk)</h3>
                        <div class="notes-container">
                            {% for note in notes %}
                                <div class="note-card vulnerable">
                                    <h4>ID: {{ note['id'] }} - {{ note['title'] | safe }}</h4>
                                    <p>{{ note['content'] | safe }}</p>
                                    <form action="/delete_vulnerable/{{ note['id'] }}" method="POST">
                                        <button type="submit">Delete</button>
                                    </form>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="column">
                        <h3>Secure Display</h3>
                        <div class="notes-container">
                            {% for note in notes %}
                                <div class="note-card secure">
                                    <h4>ID: {{ note['id'] }} - {{ note['title'] }}</h4>
                                    <p>{{ note['content'] }}</p>
                                    <form action="/delete_secure/{{ note['id'] }}" method="POST">
                                        <button type="submit">Delete</button>
                                    </form>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="column">
                    <div class="section vulnerable">
                        <h2>Vulnerable Search (SQLi Risk)</h2>
                        <form action="/search_vulnerable" method="GET">
                            <div class="form-group">
                                <label for="vuln-search">Search Title</label>
                                <input type="text" id="vuln-search" name="query" placeholder="Search by title">
                            </div>
                            <div class="form-group">
                                <button type="submit">Search (Vulnerable)</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="column">
                    <div class="section secure">
                        <h2>Secure Search</h2>
                        <form action="/search_secure" method="GET">
                            <div class="form-group">
                                <label for="secure-search">Search Title</label>
                                <input type="text" id="secure-search" name="query" placeholder="Search by title">
                            </div>
                            <div class="form-group">
                                <button type="submit">Search (Secure)</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, notes=notes)

# Vulnerable Add route: SQL Injection via direct concatenation
@app.route('/add_vulnerable', methods=['POST'])
def add_vulnerable():
    title = request.form.get('title')
    content = request.form.get('content')

    if not title or not content:
        logger.error("Missing title or content in vulnerable add")
        return render_template_string('<div class="error">Title and content are required</div>'), 400

    db = get_db()
    cursor = db.cursor()
    # VULNERABLE: Direct string concatenation for SQL Injection
    query = f"INSERT INTO notes (title, content) VALUES ('{title}', '{content}')"
    try:
        cursor.execute(query)
        db.commit()
        logger.info("Vulnerable note added successfully")
    except Exception as e:
        db.close()
        logger.error(f"Vulnerable Add Error: {str(e)}")
        return render_template_string(f'<div class="error">Vulnerable Add Error: {str(e)}</div>'), 500
    db.close()
    return index()

# Secure Add route: Parameterized query
@app.route('/add_secure', methods=['POST'])
def add_secure():
    title = request.form.get('title')
    content = request.form.get('content')

    if not title or not content:
        logger.error("Missing title or content in secure add")
        return render_template_string('<div class="error">Title and content are required</div>'), 400

    db = get_db()
    cursor = db.cursor()
    # SECURE: Parameterized query prevents SQL Injection
    query = "INSERT INTO notes (title, content) VALUES (?, ?)"
    try:
        cursor.execute(query, (title, content))
        db.commit()
        logger.info("Secure note added successfully")
    except Exception as e:
        db.close()
        logger.error(f"Secure Add Error: {str(e)}")
        return render_template_string(f'<div class="error">Secure Add Error: {str(e)}</div>'), 500
    db.close()
    return index()

# Vulnerable Delete route: SQL Injection via direct concatenation
@app.route('/delete_vulnerable/<note_id>', methods=['POST'])
def delete_vulnerable(note_id):
    db = get_db()
    cursor = db.cursor()
    # VULNERABLE: Direct string concatenation for SQL Injection
    query = f"DELETE FROM notes WHERE id = {note_id}"
    try:
        cursor.execute(query)
        if cursor.rowcount == 0:
            db.close()
            logger.warning(f"No note found with id: {note_id}")
            return render_template_string('<div class="error">Note not found</div>'), 404
        db.commit()
        logger.info("Vulnerable note deleted successfully")
    except Exception as e:
        db.close()
        logger.error(f"Vulnerable Delete Error: {str(e)}")
        return render_template_string(f'<div class="error">Vulnerable Delete Error: {str(e)}</div>'), 500
    db.close()
    return index()

# Secure Delete route: Parameterized query
@app.route('/delete_secure/<note_id>', methods=['POST'])
def delete_secure(note_id):
    db = get_db()
    cursor = db.cursor()
    # SECURE: Parameterized query prevents SQL Injection
    query = "DELETE FROM notes WHERE id = ?"
    try:
        cursor.execute(query, (note_id,))
        if cursor.rowcount == 0:
            db.close()
            logger.warning(f"No note found with id: {note_id}")
            return render_template_string('<div class="error">Note not found</div>'), 404
        db.commit()
        logger.info("Secure note deleted successfully")
    except Exception as e:
        db.close()
        logger.error(f"Secure Delete Error: {str(e)}")
        return render_template_string(f'<div class="error">Secure Delete Error: {str(e)}</div>'), 500
    db.close()
    return index()

# Vulnerable Search route: SQL Injection via direct concatenation
@app.route('/search_vulnerable', methods=['GET'])
def search_vulnerable():
    query = request.args.get('query', '')

    db = get_db()
    cursor = db.cursor()
    # VULNERABLE: Direct string concatenation for SQL Injection
    sql = f"SELECT * FROM notes WHERE title LIKE '%{query}%'"
    try:
        cursor.execute(sql)
        notes = cursor.fetchall()
        logger.info("Vulnerable search completed")
    except Exception as e:
        db.close()
        logger.error(f"Vulnerable Search Error: {str(e)}")
        return render_template_string(f'<div class="error">Vulnerable Search Error: {str(e)}</div>'), 500
    db.close()

    # Vulnerable template (XSS risk)
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vulnerable Search Results</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .notes-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }
            .note-card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: 300px;
                border-left: 5px solid #ff4444;
            }
            .note-card h4 {
                margin: 0 0 10px;
                font-size: 18px;
                color: #333;
            }
            .note-card p {
                margin: 0 0 10px;
                color: #555;
            }
            .note-card button {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .note-card button:hover {
                background-color: #cc0000;
            }
            .error {
                color: #ff4444;
                font-weight: bold;
                padding: 10px;
                background-color: #ffe6e6;
                border-radius: 5px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                color: #4CAF50;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Vulnerable Search Results for "{{ query | safe }}"</h1>
            <div class="notes-container">
                {% for note in notes %}
                    <div class="note-card">
                        <h4>ID: {{ note['id'] }} - {{ note['title'] | safe }}</h4>
                        <p>{{ note['content'] | safe }}</p>
                        <form action="/delete_vulnerable/{{ note['id'] }}" method="POST">
                            <button type="submit">Delete</button>
                        </form>
                    </div>
                {% endfor %}
            </div>
            <a href="/">Back to Home</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, notes=notes, query=query)

# Secure Search route: Parameterized query
@app.route('/search_secure', methods=['GET'])
def search_secure():
    query = request.args.get('query', '')

    db = get_db()
    cursor = db.cursor()
    # SECURE: Parameterized query prevents SQL Injection
    sql = "SELECT * FROM notes WHERE title LIKE ?"
    try:
        cursor.execute(sql, (f'%{query}%',))
        notes = cursor.fetchall()
        logger.info("Secure search completed")
    except Exception as e:
        db.close()
        logger.error(f"Secure Search Error: {str(e)}")
        return render_template_string(f'<div class="error">Secure Search Error: {str(e)}</div>'), 500
    db.close()

    # Secure template (auto-escaped)
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Secure Search Results</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .notes-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }
            .note-card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: 300px;
                border-left: 5px solid #4CAF50;
            }
            .note-card h4 {
                margin: 0 0 10px;
                font-size: 18px;
                color: #333;
            }
            .note-card p {
                margin: 0 0 10px;
                color: #555;
            }
            .note-card button {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .note-card button:hover {
                background-color: #cc0000;
            }
            .error {
                color: #ff4444;
                font-weight: bold;
                padding: 10px;
                background-color: #ffe6e6;
                border-radius: 5px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                color: #4CAF50;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Secure Search Results for "{{ query }}"</h1>
            <div class="notes-container">
                {% for note in notes %}
                    <div class="note-card">
                        <h4>ID: {{ note['id'] }} - {{ note['title'] }}</h4>
                        <p>{{ note['content'] }}</p>
                        <form action="/delete_secure/{{ note['id'] }}" method="POST">
                            <button type="submit">Delete</button>
                        </form>
                    </div>
                {% endfor %}
            </div>
            <a href="/">Back to Home</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, notes=notes, query=escape(query))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
