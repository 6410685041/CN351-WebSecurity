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


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         to = request.form['to']
#         subject = request.form['subject']
#         message = request.form['message']

#         msg = MIMEText(message)
#         msg['Subject'] = subject
#         msg['From'] = 'user@example.com'
#         msg['To'] = to

#         try:
#             with smtplib.SMTP('localhost', 1025) as server:
#                 server.sendmail('user@example.com', [to], msg.as_string())
#             return "Message sent!"
#         except Exception as e:
#             return f"Failed to send message: {e}"
#     return render_template('contact.html')

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


@app.route('/xss', methods=['GET', 'POST'])
def xss():
    text = request.args.get('txt')
    if text:
        response = f"Login successful! {text}"
        return render_template_string(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>XSS</title>
        </head>
        <body>
            <h1>{response}</h1>
            <form method="get" action="/xss">
                Text: <input type="text" name="txt"><br>
                <input type="submit" value="Add">
            </form>
        </body>
        </html>
        """)
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>XSS</title>
    </head>
    <body>
        <h1>Welcome to the xss Page</h1>
        <form method="get" action="/xss">
            Text: <input type="text" name="txt"><br>
            <input type="submit" value="Add">
        </form>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
