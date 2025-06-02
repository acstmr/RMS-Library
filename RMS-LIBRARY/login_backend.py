from flask import Flask, render_template, request, redirect, session, flash, make_response
import hashlib
from functools import wraps

from db import db, cursor
from admin_backend import admin_bp  
from librarian_backend import librarian_bp  
from utils import no_cache

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(librarian_bp, url_prefix='/librarian')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM lb_users WHERE username=%s AND password=%s", (username, password_hash))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/dashboard')
        else:
            error = 'Invalid username or password'
            flash(error, 'error')

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', '').strip()

        if not username or not password or not full_name or not role:
            error = 'Please fill in all required fields.'
            flash(error, 'error')
            return render_template('register.html', error=error)

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM lb_users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = 'Username already taken.'
            flash(error, 'error')
        else:
            try:
                cursor.execute(
                    "INSERT INTO lb_users (username, password, full_name, role) VALUES (%s, %s, %s, %s)",
                    (username, password_hash, full_name, role)
                )
                db.commit()
                flash("Registration successful! Please login.", "success")
                return redirect('/')
            except Exception as e:
                db.rollback()
                error = f"Database error: {e}"
                flash(error, 'error')

    return render_template('register.html', error=error)

@app.route('/dashboard')
@no_cache
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    role = session.get('role')

    if role == 'admin':
        return render_template('admin_dashboard.html', username=session.get('username'))
    elif role == 'librarian':
        return render_template('librarian_dashboard.html', username=session.get('username'))
    else:
        return "Unauthorized", 403

@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect('/'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)
