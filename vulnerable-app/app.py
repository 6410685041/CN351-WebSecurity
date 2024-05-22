from flask import Flask, request, render_template
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            return f"Login successful! {username}"
        else:
            return "Invalid username or password"
    return render_template('login.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        message = request.form['message']

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = 'user@example.com'
        msg['To'] = to

        try:
            with smtplib.SMTP('localhost', 1025) as server:
                server.sendmail('user@example.com', [to], msg.as_string())
            return "Message sent!"
        except Exception as e:
            return f"Failed to send message: {e}"
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        query = "SELECT * FROM users WHERE username = ?"
        existing_user = conn.execute(query, (username,)).fetchone()
        if existing_user:
            conn.close()
            return "Username already taken"
        else:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return "User registered successfully"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
