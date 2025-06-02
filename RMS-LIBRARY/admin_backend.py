from flask import Blueprint, render_template, request, redirect, session, flash
from functools import wraps
from db import db, cursor
from utils import no_cache

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/students-admin')
@admin_required
@no_cache
def students_admin():
    cursor.execute("SELECT * FROM lb_students")
    students = cursor.fetchall()
    return render_template('students-admin.html', students=students)

@admin_bp.route('/add-student', methods=['GET', 'POST'])
@admin_required
@no_cache
def add_student():
    if request.method == 'POST':
        try:
            student_data = (
                request.form['student_number'],
                request.form['student_full_name'],
                request.form['student_course'],
                request.form['student_year_level'],
                request.form['student_email'],
                request.form['student_contact_number'],
                request.form['student_address']
            )
            cursor.execute("""
                INSERT INTO lb_students (
                    student_number, student_full_name, student_course, student_year_level,
                    student_email, student_contact_number, student_address
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, student_data)
            db.commit()
            flash("Student added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash("Failed to add student.", "error")
        return redirect('/admin/students-admin')

    return render_template('add-student.html')

@admin_bp.route('/update-student/<int:student_id>', methods=['GET', 'POST'])
@admin_required
@no_cache
def update_student(student_id):
    if request.method == 'POST':
        try:
            student_data = (
                request.form['student_number'],
                request.form['student_full_name'],
                request.form['student_course'],
                request.form['student_year_level'],
                request.form['student_email'],
                request.form['student_contact_number'],
                request.form['student_address'],
                student_id
            )
            cursor.execute("""
                UPDATE lb_students SET
                    student_number=%s, student_full_name=%s, student_course=%s,
                    student_year_level=%s, student_email=%s, student_contact_number=%s,
                    student_address=%s
                WHERE student_id=%s
            """, student_data)
            db.commit()
            flash("Student updated successfully.", "success")
        except Exception as e:
            db.rollback()
            flash("Failed to update student.", "error")
        return redirect('/admin/students-admin')

    cursor.execute("SELECT * FROM lb_students WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    return render_template('update-student.html', student=student)

@admin_bp.route('/delete-student/<int:student_id>', methods=['POST'])
@admin_required
@no_cache
def delete_student(student_id):
    try:
        cursor.execute("DELETE FROM lb_students WHERE student_id=%s", (student_id,))
        db.commit()
        flash("Student deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash("Failed to delete student.", "error")
    return redirect('/admin/students-admin')

@admin_bp.route('/books-admin')
@admin_required
@no_cache
def books_admin():
    cursor.execute("SELECT * FROM lb_books")
    books = cursor.fetchall()
    return render_template('books-admin.html', books=books)

@admin_bp.route('/add-book', methods=['GET', 'POST'])
@admin_required
@no_cache
def add_book():
    if request.method == 'POST':
        try:
            book_data = (
                request.form['book_title'],
                request.form['book_author'],
                request.form['book_publisher'],
                request.form['book_category'],
                request.form['shelf_number'],
                request.form['status']
            )
            cursor.execute("""
                INSERT INTO lb_books (
                    book_title, book_author, book_publisher,
                    book_category, shelf_number, status
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, book_data)
            db.commit()
            flash("Book added successfully.", "success")
        except Exception as e:
            db.rollback()
            flash("Failed to add book.", "error")
        return redirect('/admin/books-admin')

    return render_template('add-book.html')

@admin_bp.route('/update-book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
@no_cache
def update_book(book_id):
    if request.method == 'POST':
        try:
            book_data = (
                request.form['book_title'],
                request.form['book_author'],
                request.form['book_publisher'],
                request.form['book_category'],
                request.form['shelf_number'],
                request.form['status'],
                book_id
            )
            cursor.execute("""
                UPDATE lb_books SET
                    book_title=%s, book_author=%s, book_publisher=%s,
                    book_category=%s, shelf_number=%s, status=%s
                WHERE book_id=%s
            """, book_data)
            db.commit()
            flash("Book updated successfully.", "success")
        except Exception as e:
            db.rollback()
            flash("Failed to update book.", "error")
        return redirect('/admin/books-admin')

    cursor.execute("SELECT * FROM lb_books WHERE book_id=%s", (book_id,))
    book = cursor.fetchone()
    return render_template('update-book.html', book=book)

@admin_bp.route('/delete-book/<int:book_id>', methods=['POST'])
@admin_required
@no_cache
def delete_book(book_id):
    try:
        cursor.execute("DELETE FROM lb_books WHERE book_id=%s", (book_id,))
        db.commit()
        flash("Book deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash("Failed to delete book.", "error")
    return redirect('/admin/books-admin')
