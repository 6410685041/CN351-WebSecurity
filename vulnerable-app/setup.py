import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
c.execute("INSERT INTO users (username, password) VALUES ('user1', 'password1')")

conn.commit()
conn.close()

print("Database setup complete.")
