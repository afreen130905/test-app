from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute("INSERT INTO users VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # ❌ Vulnerable to SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = c.execute(query).fetchone()

    if result:
        return redirect('/home')
    else:
        return "Login Failed"

@app.route('/home', methods=['GET', 'POST'])
def home():
    comment = ""
    if request.method == 'POST':
        comment = request.form['comment']  # ❌ Vulnerable to XSS

    return render_template('home.html', comment=comment)

if __name__ == '__main__':
    app.run(debug=True)