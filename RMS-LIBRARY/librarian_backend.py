from flask import Blueprint, render_template, request, redirect, session, flash
from db import db, cursor
from datetime import datetime

librarian_bp = Blueprint('librarian_bp', __name__, template_folder='templates')

def record_exists(table, column, value):
    """Check if a specific record exists in a table."""
    dict_cursor = db.cursor(dictionary=True)
    dict_cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
    return dict_cursor.fetchone() is not None

@librarian_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')
    return render_template('librarian_dashboard.html', username=session.get('username'))

@librarian_bp.route('/borrow-transactions')
def borrow_transactions():
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    dict_cursor = db.cursor(dictionary=True)

    dict_cursor.execute("SELECT book_id FROM lb_books WHERE status = 'available'")
    books = dict_cursor.fetchall()

    dict_cursor.execute("SELECT student_id FROM lb_students")
    students = dict_cursor.fetchall()

    dict_cursor.execute("""
        SELECT transaction_id, book_id, student_id, borrow_date, due_date, return_date, status
        FROM lb_borrow_transactions
    """)
    transactions = dict_cursor.fetchall()

    return render_template('borrow-transactions.html',
                           transactions=transactions,
                           books=books,
                           students=students,
                           username=session.get('username'))

@librarian_bp.route('/add-transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    book_id = request.form.get('book_id')
    student_id = request.form.get('student_id')
    borrow_date = request.form.get('borrow_date')
    due_date = request.form.get('due_date')
    status = request.form.get('status', 'borrowed')

    if not all([book_id, student_id, borrow_date, due_date]):
        flash("Please fill in all required fields.", "error")
        return redirect('/librarian/borrow-transactions')

    if not record_exists('lb_books', 'book_id', book_id):
        flash("Error: Book ID does not exist.", "error")
        return redirect('/librarian/borrow-transactions')

    if not record_exists('lb_students', 'student_id', student_id):
        flash("Error: Student ID does not exist.", "error")
        return redirect('/librarian/borrow-transactions')

    dict_cursor = db.cursor(dictionary=True)
    dict_cursor.execute("SELECT status FROM lb_books WHERE book_id = %s", (book_id,))
    book = dict_cursor.fetchone()
    if book is None or book['status'] != 'available':
        flash("Error: Book is currently not available for borrowing.", "error")
        return redirect('/librarian/borrow-transactions')

    try:
        cursor.execute("""
            INSERT INTO lb_borrow_transactions (book_id, student_id, borrow_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (book_id, student_id, borrow_date, due_date, status))

        cursor.execute("UPDATE lb_books SET status = 'borrowed' WHERE book_id = %s", (book_id,))
        db.commit()
        flash("Transaction added successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/borrow-transactions')

@librarian_bp.route('/update-transaction/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    book_id = request.form.get('book_id')
    student_id = request.form.get('student_id')
    borrow_date = request.form.get('borrow_date')
    due_date = request.form.get('due_date')
    return_date = request.form.get('return_date') or None
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

            dict_cursor = db.cursor(dictionary=True)
            dict_cursor.execute("SELECT due_date FROM lb_borrow_transactions WHERE transaction_id = %s", (transaction_id,))
            result = dict_cursor.fetchone()
            if result and return_date:
                due_date_db = result['due_date']
                return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

                if isinstance(due_date_db, datetime):
                    due_date_obj = due_date_db
                else:
                    due_date_obj = datetime.strptime(str(due_date_db), "%Y-%m-%d")

                days_late = (return_date_obj - due_date_obj).days
                if days_late > 0:
                    duty_hours = days_late * 0.25  
                    cursor.execute("""
                        INSERT INTO lb_penalties (transaction_id, days_late, duty_hours, is_served)
                        VALUES (%s, %s, %s, %s)
                    """, (transaction_id, days_late, duty_hours, 0))
        elif status == 'borrowed':
            cursor.execute("UPDATE lb_books SET status = 'borrowed' WHERE book_id = %s", (book_id,))

        db.commit()
        flash("Transaction updated successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/borrow-transactions')

@librarian_bp.route('/delete-transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    try:
        cursor.execute("DELETE FROM lb_borrow_transactions WHERE transaction_id = %s", (transaction_id,))
        db.commit()
        flash("Transaction deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash(f"Database error: {e}", "error")

    return redirect('/librarian/borrow-transactions')

@librarian_bp.route('/penalties')
def penalties():
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    dict_cursor = db.cursor(dictionary=True)
    

    dict_cursor.execute("""
        SELECT 
            p.*,
            bt.book_id,
            bt.student_id,
            bt.borrow_date,
            bt.due_date,
            bt.return_date,
            b.book_title,
            b.book_author,
            s.student_full_name,
            s.student_number,
            s.student_course
        FROM lb_penalties p
        JOIN lb_borrow_transactions bt ON p.transaction_id = bt.transaction_id
        JOIN lb_books b ON bt.book_id = b.book_id
        JOIN lb_students s ON bt.student_id = s.student_id
        ORDER BY p.is_served ASC, p.penalty_id DESC
    """)
    penalties = dict_cursor.fetchall()

    total_penalties = len(penalties)
    pending_penalties = sum(1 for p in penalties if not p['is_served'])
    total_duty_hours = sum(p['duty_hours'] for p in penalties)

    return render_template('penalties.html', 
                         penalties=penalties,
                         username=session.get('username'),
                         stats={
                             'total_penalties': total_penalties,
                             'pending_penalties': pending_penalties,
                             'total_duty_hours': total_duty_hours
                         })

@librarian_bp.route('/edit-penalty/<int:penalty_id>', methods=['GET', 'POST'])
def edit_penalty(penalty_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return redirect('/')

    dict_cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        is_served = request.form.get('is_served', '0')  # Default to '0' if not provided
        is_served_value = 1 if is_served == '1' else 0

        try:
            cursor.execute("UPDATE lb_penalties SET is_served = %s WHERE penalty_id = %s", (is_served_value, penalty_id))
            db.commit()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {'success': True, 'message': 'Penalty status updated successfully'}
            
            flash("Penalty status updated successfully.", "success")
            return redirect('/librarian/penalties')
        except Exception as e:
            db.rollback()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {'error': str(e)}, 500
            flash(f"Database error: {e}", "error")
            return redirect('/librarian/penalties')

    dict_cursor.execute("""
        SELECT p.*, 
               bt.book_id, bt.student_id, bt.borrow_date, bt.due_date, bt.return_date,
               b.book_title, b.book_author,
               s.student_full_name, s.student_number, s.student_course
        FROM lb_penalties p
        JOIN lb_borrow_transactions bt ON p.transaction_id = bt.transaction_id
        JOIN lb_books b ON bt.book_id = b.book_id
        JOIN lb_students s ON bt.student_id = s.student_id
        WHERE p.penalty_id = %s
    """, (penalty_id,))
    penalty = dict_cursor.fetchone()
    
    if not penalty:
        flash("Penalty not found.", "error")
        return redirect('/librarian/penalties')

    return render_template('edit-penalty.html', penalty=penalty)

@librarian_bp.route('/get-book-details/<int:book_id>')
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
def get_student_details(student_id):
    if 'user_id' not in session or session.get('role') != 'librarian':
        return {'error': 'Unauthorized'}, 401

    dict_cursor = db.cursor(dictionary=True)
    dict_cursor.execute("""
        SELECT s.*, 
               COUNT(CASE WHEN bt.status = 'borrowed' THEN 1 END) as active_borrows
        FROM lb_students s
        LEFT JOIN lb_borrow_transactions bt ON s.student_id = bt.student_id
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
