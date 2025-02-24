import sqlite3
from hashlib import sha256
import secrets
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'REDACTED'
limiter = Limiter(key_func=get_remote_address, app=app)

def get_db_connection():
    conn = sqlite3.connect('grades.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()

        if user:
            # Ensure the row is accessed safely
            reset_token_expires_at = user['reset_token_expires_at']
            current_time = datetime.utcnow()

            # Convert reset_token_expires_at to a datetime object if it's a string
            if isinstance(reset_token_expires_at, str):
                reset_token_expires_at = datetime.fromisoformat(reset_token_expires_at)

            if reset_token_expires_at and current_time <= reset_token_expires_at:
                # Token is still valid, so no need to generate a new one
                send_reset_email(user['email'], user['reset_token'])
            else:
                # Generate a new reset token and set its expiration time
                reset_token = secrets.token_hex(16)
                reset_token_expires_at = current_time + timedelta(minutes=10)

                # Update the user's record with the new token and expiration time
                c.execute(
                    'UPDATE users SET reset_token = ?, reset_token_expires_at = ? WHERE username = ?',
                    (reset_token, reset_token_expires_at.isoformat(), username)  # Store as ISO format string
                )
                conn.commit()

                # Send the reset email with the new token
                send_reset_email(user['email'], reset_token)

            conn.close()
            return redirect(url_for('login'))
        else:
            conn.close()
            return redirect(url_for('login'))  # User not found, but no feedback provided

    return render_template('reset_password.html')

def send_reset_email(email, reset_token):
    print(f"Sending password reset email to {email} with token: {reset_token}")


@app.route('/grades', methods=['GET', 'POST'])
@limiter.limit("2000/minute") 
def grades():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if not search_query:
            flash('Please enter a search query.', 'info')
            return render_template('grades.html', results=None)

        conn = get_db_connection()
        c = conn.cursor()

        
        query = f"SELECT * FROM grades WHERE username LIKE '%{search_query}%'"
        try:
            c.execute(query)
            results = c.fetchall()

            
            if results:
                if 'username' in session and session['username'] == 'admin':
                    return render_template('grades.html', results=results)
                else:
                    flash('You need to be authenticated to see results !', 'info')
            else:
                flash('No results found.', 'error')

        except sqlite3.Error as e:
            flash(f"SQL Error: {e}", 'error')

        conn.close()

    return render_template('grades.html', results=None)


@app.route('/update-password/<reset_token>', methods=['GET', 'POST'])
def update_password(reset_token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE reset_token = ?', (reset_token,))
        user = c.fetchone()

        if user:
            hashed_password = sha256(new_password.encode()).hexdigest()
            c.execute('UPDATE users SET password = ?, reset_token = NULL WHERE reset_token = ?', (hashed_password, reset_token))
            conn.commit()
            conn.close()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired reset token.', 'error')

    return render_template('update_password.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or session['username'] != 'admin':
        flash('You must be logged in as an admin to access this page.', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()

    return render_template('admin.html', users=users)


@app.before_request
def block_automated_tools():
    user_agent = request.headers.get('User-Agent', '')
    if 'sqlmap' in user_agent.lower() or 'scanner' in user_agent.lower():
        return "Access Denied", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False)
