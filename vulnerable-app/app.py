from flask import Flask, request, render_template, render_template_string
import sqlite3
import smtplib
import logging
from email.mime.text import MIMEText

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def index():
    text = request.args.get('txt')
    
    if text:
        logging.debug("User input: " + text)
        return "Check the logs for the input!"
    return render_template('index.html')

@app.route('/member', methods=['GET'])
def member():
    return render_template('member.html')


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
            response = f"Login successful! {username}"
            return render_template('login.html', response=response)
        else:
            response = "Invalid username or password"
            return render_template('login.html', response=response)
    return render_template('login.html')

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
            response = "Username already taken"
            return render_template('register.html', response=response)
        else:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            response = "User registered successfully"
            return render_template('register.html', response=response)
    return render_template('register.html')


@app.route('/xss', methods=['GET', 'POST'])
def xss():
    text = request.args.get('txt')
    if text:
        response = f"Comment: {text}"
        return render_template('xss.html', response=response)
    return render_template('xss.html')

if __name__ == '__main__':
    app.run(debug=True)
