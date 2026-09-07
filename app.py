from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from dotenv import load_dotenv   # New import

load_dotenv()   # This reads your .env file

app = Flask(__name__)
app.secret_key = 'signvani-secret-key-2026'

# Database setup
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
        conn.commit()
        conn.close()

init_db()

# Routes (keep all your existing routes exactly as they are)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['user'])

@app.route('/alphabet')
def alphabet():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('alphabet.html')

@app.route('/numbers')
def numbers():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('numbers.html')

@app.route('/tutorials')
def tutorials():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('tutorials.html')

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/translator')
def translator():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('translator.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Updated clean startup
if __name__ == '__main__':
    print("\n🚀 SignVani - ISL Learning Website Started Successfully!")
    print("🌐 Open this link in your browser:")
    print("   http://127.0.0.1:5000")
    print("👤 Register or Login to start learning alphabets and use the translator.\n")
    
    app.run(debug=True, use_reloader=False)