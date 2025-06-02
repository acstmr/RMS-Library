from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone
from db import db, cursor
from utils import no_cache

librarian_bp = Blueprint('librarian_bp', __name__, template_folder='templates')

def librarian_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'librarian':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def record_exists(table, column, value):
    dict_cursor = db.cursor(dictionary=True)
    dict_cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
    return dict_cursor.fetchone() is not None

@librarian_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')
    return render_template('librarian_dashboard.html', username=session.get('username'))

@librarian_bp.route('/borrow-transactions')
@librarian_required
@no_cache
def borrow_transactions():
    cursor.execute("""
        SELECT bt.*, 
               s.student_full_name, s.student_number, s.student_course,
               b.book_title, b.book_author, b.book_publisher, b.book_category
        FROM lb_borrow_transactions bt
        JOIN lb_students s ON bt.student_id = s.student_id
        JOIN lb_books b ON bt.book_id = b.book_id
        ORDER BY bt.transaction_id DESC
    """)
    transactions = cursor.fetchall()

    cursor.execute("SELECT * FROM lb_students ORDER BY student_full_name")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM lb_books WHERE status = 'available' ORDER BY book_title")
    books = cursor.fetchall()

    return render_template('borrow-transactions.html', 
                         transactions=transactions,
                         students=students,
                         books=books,
                         username=session.get('username'))

@librarian_bp.route('/add-transaction', methods=['POST'])
@librarian_required
@no_cache
def add_transaction():
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    book_id = request.form.get('book_id')
    student_id = request.form.get('student_id')
    borrow_date = request.form.get('borrow_date')
    due_date = request.form.get('due_date')

    if not all([book_id, student_id, borrow_date, due_date]):
        flash("Please fill in all required fields.", "error")
        return redirect('/librarian/borrow-transactions')

    if not record_exists('lb_books', 'book_id', book_id):
        flash("Error: Book ID does not exist.", "error")
        return redirect('/librarian/borrow-transactions')

    if not record_exists('lb_students', 'student_id', student_id):
        flash("Error: Student ID does not exist.", "error")
        return redirect('/librarian/borrow-transactions')

    try:
        cursor.execute("""
            INSERT INTO lb_borrow_transactions (
                book_id, student_id, borrow_date, due_date, status
            ) VALUES (%s, %s, %s, %s, %s)
        """, (book_id, student_id, borrow_date, due_date, 'borrowed'))

        cursor.execute("UPDATE lb_books SET status = 'borrowed' WHERE book_id = %s", (book_id,))
        
        db.commit()
        flash("Transaction added successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/borrow-transactions')

@librarian_bp.route('/update-transaction/<int:transaction_id>', methods=['POST'])
@librarian_required
@no_cache
def update_transaction(transaction_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    book_id = request.form.get('book_id')
    student_id = request.form.get('student_id')
    borrow_date = request.form.get('borrow_date')
    due_date = request.form.get('due_date')
    return_date = request.form.get('return_date')
    status = request.form.get('status')

    if not all([book_id, student_id, borrow_date, due_date, status]):
        flash("Please fill in all required fields.", "error")
        return redirect('/librarian/borrow-transactions')

    if not record_exists('lb_books', 'book_id', book_id):
        flash("Error: Book ID does not exist.", "error")
        return redirect('/librarian/borrow-transactions')

    if not record_exists('lb_students', 'student_id', student_id):
        flash("Error: Student ID does not exist.", "error")
        return redirect('/librarian/borrow-transactions')

    try:
        if status == 'returned' and not return_date:
            return_date = datetime.now().strftime('%Y-%m-%d')

        cursor.execute("""
            UPDATE lb_borrow_transactions SET
                book_id = %s,
                student_id = %s,
                borrow_date = %s,
                due_date = %s,
                return_date = %s,
                status = %s
            WHERE transaction_id = %s
        """, (book_id, student_id, borrow_date, due_date, return_date, status, transaction_id))

        if status == 'returned':
            cursor.execute("UPDATE lb_books SET status = 'available' WHERE book_id = %s", (book_id,))

            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")
            days_late = (return_date_obj - due_date_obj).days

            if days_late > 0:
                duty_hours = days_late * 1.0
                cursor.execute("SELECT penalty_id FROM lb_penalties WHERE transaction_id = %s", (transaction_id,))
                existing_penalty = cursor.fetchone()

                if existing_penalty:
                    cursor.execute("""
                        UPDATE lb_penalties 
                        SET days_late = %s, duty_hours = %s 
                        WHERE transaction_id = %s
                    """, (days_late, duty_hours, transaction_id))
                else:
                    cursor.execute("""
                        INSERT INTO lb_penalties (transaction_id, days_late, duty_hours, is_served)
                        VALUES (%s, %s, %s, %s)
                    """, (transaction_id, days_late, duty_hours, 0))

        elif status == 'borrowed':
            cursor.execute("UPDATE lb_books SET status = 'borrowed' WHERE book_id = %s", (book_id,))
            cursor.execute("DELETE FROM lb_penalties WHERE transaction_id = %s", (transaction_id,))

        db.commit()
        flash("Transaction updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/borrow-transactions')

@librarian_bp.route('/delete-transaction/<int:transaction_id>', methods=['POST'])
@librarian_required
@no_cache
def delete_transaction(transaction_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    try:
        cursor.execute("SELECT book_id, status FROM lb_borrow_transactions WHERE transaction_id = %s", (transaction_id,))
        transaction = cursor.fetchone()
        
        if transaction and transaction['status'] == 'borrowed':
            cursor.execute("UPDATE lb_books SET status = 'available' WHERE book_id = %s", (transaction['book_id'],))

        cursor.execute("DELETE FROM lb_borrow_transactions WHERE transaction_id = %s", (transaction_id,))
        db.commit()
        flash("Transaction deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/borrow-transactions')

@librarian_bp.route('/penalties')
@librarian_required
@no_cache
def penalties():
    cursor.execute("""
        SELECT p.*, bt.student_id, s.student_full_name, s.student_number,
               bt.book_id, b.book_title, b.book_author, bt.due_date, bt.return_date
        FROM lb_penalties p
        JOIN lb_borrow_transactions bt ON p.transaction_id = bt.transaction_id
        JOIN lb_students s ON bt.student_id = s.student_id
        JOIN lb_books b ON bt.book_id = b.book_id
        ORDER BY p.penalty_id DESC
    """)
    penalties = cursor.fetchall()

    total_penalties = len(penalties)
    pending_penalties = sum(1 for p in penalties if not p['is_served'])
    total_duty_hours = sum(p['duty_hours'] for p in penalties)

    stats = {
        'total_penalties': total_penalties,
        'pending_penalties': pending_penalties,
        'total_duty_hours': total_duty_hours
    }

    return render_template('penalties.html', penalties=penalties, stats=stats, username=session.get('username'))

@librarian_bp.route('/update-penalty/<int:penalty_id>', methods=['POST'])
@librarian_required
@no_cache
def update_penalty(penalty_id):
    try:
        status = request.form.get('status')
        if status is None:
            flash("Status is required", "error")
            return redirect('/librarian/penalties')
            
        is_served = 1 if status.lower() == 'served' else 0
        cursor.execute("UPDATE lb_penalties SET is_served = %s WHERE penalty_id = %s", (is_served, penalty_id))
        db.commit()
        flash("Penalty status updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/penalties')

@librarian_bp.route('/edit-penalty/<int:penalty_id>', methods=['POST'])
@librarian_required
@no_cache
def edit_penalty(penalty_id):
    try:
        is_served = request.form.get('is_served')
        if is_served is None:
            return jsonify({'error': 'Status is required'}), 400
            
        cursor.execute("UPDATE lb_penalties SET is_served = %s WHERE penalty_id = %s", (is_served, penalty_id))
        db.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Penalty status updated successfully'})
            
        flash("Penalty status updated successfully.", "success")
        return redirect('/librarian/penalties')
    except Exception as e:
        db.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': str(e)}), 500
        flash(f"Database error: {e}", "error")
        return redirect('/librarian/penalties')

@librarian_bp.route('/get-book-details/<int:book_id>')
@librarian_required
@no_cache
def get_book_details(book_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return {'error': 'Unauthorized'}, 401

    dict_cursor = db.cursor(dictionary=True)
    dict_cursor.execute("""
        SELECT book_id, book_title, book_author, status
        FROM lb_books 
        WHERE book_id = %s
    """, (book_id,))
    book = dict_cursor.fetchone()
    
    if book:
        return book
    return {'error': 'Book not found'}, 404

@librarian_bp.route('/get-student-details/<int:student_id>')
@librarian_required
@no_cache
def get_student_details(student_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return {'error': 'Unauthorized'}, 401

    dict_cursor = db.cursor(dictionary=True)
    dict_cursor.execute("""
        SELECT s.*, COUNT(bt.transaction_id) as active_borrows
        FROM lb_students s
        LEFT JOIN lb_borrow_transactions bt ON s.student_id = bt.student_id AND bt.status = 'borrowed'
        WHERE s.student_id = %s
        GROUP BY s.student_id
    """, (student_id,))
    student = dict_cursor.fetchone()
    
    if student:
        return student
    return {'error': 'Student not found'}, 404

@librarian_bp.route('/delete-penalty/<int:penalty_id>', methods=['POST'])
def delete_penalty(penalty_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return {'error': 'Unauthorized'}, 401

    try:
        cursor.execute("DELETE FROM lb_penalties WHERE penalty_id = %s", (penalty_id,))
        db.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'success': True, 'message': 'Penalty deleted successfully'}
            
        flash("Penalty deleted successfully.", "success")
        return redirect('/librarian/penalties')
    except Exception as e:
        db.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'error': str(e)}, 500
        flash(f"Database error: {e}", "error")
        return redirect('/librarian/penalties')
