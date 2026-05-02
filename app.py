"""
Fake Job Detection System - Flask Application
==============================================
Main Flask application file containing all routes and business logic.
Handles authentication, job posting, fake detection, and admin dashboard.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from config.database import get_db, close_db, init_db

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# Register database teardown handler
app.teardown_appcontext(close_db)


# ============================================
# Rule-Based Fake Job Detection Algorithm
# ============================================
def calculate_fake_score(job_data):
    """
    Calculate fake job detection score based on predefined rules.
    
    Scoring Rules:
    - Gmail/Yahoo email addresses: +2 points
    - Salary exceeding $100,000: +2 points
    - Job description contains "fee", "registration", or "urgent hiring": +3 points
    - Empty location field: +1 point
    
    Classification Thresholds:
    - 0-2 points: Genuine
    - 3-5 points: Suspicious
    - 6+ points: Fake
    
    Args:
        job_data (dict): Dictionary containing job posting data with keys:
            - email: Employer email address
            - salary: Job salary (float or string)
            - job_description: Job description text
            - location: Job location (string)
    
    Returns:
        tuple: (score (int), classification (str))
    """
    score = 0
    
    # Rule 1: Check for Gmail/Yahoo email addresses (+2 points)
    email = job_data.get('email', '').lower()
    if '@gmail.com' in email or '@yahoo.com' in email:
        score += 2
    
    # Rule 2: Check if salary exceeds $100,000 (+2 points)
    try:
        salary = float(job_data.get('salary', 0))
        if salary > 100000:
            score += 2
    except (ValueError, TypeError):
        pass  # If salary is invalid, skip this rule
    
    # Rule 3: Check job description for suspicious keywords (+3 points)
    job_description = job_data.get('job_description', '').lower()
    suspicious_keywords = ['fee', 'registration', 'urgent hiring']
    if any(keyword in job_description for keyword in suspicious_keywords):
        score += 3
    
    # Rule 4: Check if location field is empty (+1 point)
    location = job_data.get('location', '').strip()
    if not location:
        score += 1
    
    # Determine classification based on score
    if score <= 2:
        classification = 'Genuine'
    elif score <= 5:
        classification = 'Suspicious'
    else:  # score >= 6
        classification = 'Fake'
    
    return score, classification


# ============================================
# Authentication Routes
# ============================================
@app.route('/control-center')
def control_center():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Example stats; plug in real queries later
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) AS c FROM jobs")
        jobs_count = cur.fetchone()['c']

        cur.execute("SELECT COUNT(*) AS c FROM jobs WHERE detection_score >= 6")
        high_risk_count = cur.fetchone()['c']

        cur.execute("SELECT COUNT(*) AS c FROM jobs WHERE classification = 'Suspicious'")
        suspicious_count = cur.fetchone()['c']

        suspicious_rate = f"{round((suspicious_count / jobs_count) * 100)}%" if jobs_count else "0%"

        cur.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC LIMIT 30"
        )
        jobs = cur.fetchall()
        cur.close()
    except Exception:
        jobs_count = 0
        high_risk_count = 0
        suspicious_rate = "0%"
        jobs = []

    return render_template(
        'saas_shell.html',
        jobs=jobs,
        jobs_count=jobs_count,
        high_risk_count=high_risk_count,
        suspicious_rate=suspicious_rate,
    )
@app.route('/')
def index():
    """Redirect to login page"""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login (both employers and admins).
    Supports both regular form submission and AJAX requests.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user_type = request.form.get('user_type', 'employer')  # 'employer' or 'admin'
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please fill in all fields'}), 400
            return render_template('login.html')
        
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            
            # Query appropriate table based on user type
            if user_type == 'admin':
                cursor.execute(
                    "SELECT * FROM admins WHERE username = %s OR email = %s",
                    (username, username)
                )
            else:
                cursor.execute(
                    "SELECT * FROM employers WHERE username = %s OR email = %s",
                    (username, username)
                )
            
            user = cursor.fetchone()
            cursor.close()
            
            if user and check_password_hash(user['password_hash'], password):
                # Login successful
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_type'] = user_type
                
                if request.is_json:
                    return jsonify({
                        'success': True,
                        'message': 'Login successful',
                        'redirect': url_for('admin_dashboard' if user_type == 'admin' else 'job_list')
                    })
                
                # Redirect based on user type
                if user_type == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('job_list'))
            else:
                flash('Invalid username or password', 'error')
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
                
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Database error occurred'}), 500
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle employer registration.
    Creates new employer account with password hashing.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        company_name = request.form.get('company_name', '').strip()
        
        # Validation
        if not all([username, email, password, confirm_password, company_name]):
            flash('Please fill in all fields', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please fill in all fields'}), 400
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
            return render_template('register.html')
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Invalid email format', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400
            return render_template('register.html')
        
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Check if username or email already exists
            cursor.execute(
                "SELECT id FROM employers WHERE username = %s OR email = %s",
                (username, email)
            )
            if cursor.fetchone():
                flash('Username or email already exists', 'error')
                cursor.close()
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Username or email already exists'}), 400
                return render_template('register.html')
            
            # Hash password and insert new employer
            password_hash = generate_password_hash(password)
            cursor.execute(
                """INSERT INTO employers (username, email, password_hash, company_name)
                   VALUES (%s, %s, %s, %s)""",
                (username, email, password_hash, company_name)
            )
            db.commit()
            cursor.close()
            
            flash('Registration successful! Please login.', 'success')
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Registration successful',
                    'redirect': url_for('login')
                })
            
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Database error occurred'}), 500
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============================================
# Job Posting Routes
# ============================================

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    """
    Handle job posting by employers.
    Automatically calculates fake detection score and classification.
    """
    # Check if user is logged in as employer
    if 'user_id' not in session or session.get('user_type') != 'employer':
        flash('Please login as an employer to post jobs', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        company_name = request.form.get('company_name', '').strip()
        email = request.form.get('email', '').strip()
        job_title = request.form.get('job_title', '').strip()
        salary = request.form.get('salary', '').strip()
        location = request.form.get('location', '').strip()
        job_description = request.form.get('job_description', '').strip()
        contact_details = request.form.get('contact_details', '').strip()
        
        # Validation
        if not all([company_name, email, job_title, job_description]):
            flash('Please fill in all required fields', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
            return render_template('post_job.html')
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Invalid email format', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400
            return render_template('post_job.html')
        
        # Convert salary to float if provided
        try:
            salary_float = float(salary) if salary else None
        except ValueError:
            salary_float = None
        
        # Calculate fake detection score
        job_data = {
            'email': email,
            'salary': salary_float,
            'job_description': job_description,
            'location': location
        }
        score, classification = calculate_fake_score(job_data)
        
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Insert job posting
            cursor.execute(
                """INSERT INTO jobs (employer_id, company_name, email, job_title, salary, 
                   location, job_description, contact_details, detection_score, classification)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (session['user_id'], company_name, email, job_title, salary_float,
                 location, job_description, contact_details, score, classification)
            )
            db.commit()
            cursor.close()
            
            flash(f'Job posted successfully! Classification: {classification} (Score: {score})', 'success')
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': f'Job posted successfully! Classification: {classification}',
                    'score': score,
                    'classification': classification
                })
            
            return redirect(url_for('job_list'))
            
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            if request.is_json:
                return jsonify({'success': False, 'message': 'Database error occurred'}), 500
    
    return render_template('post_job.html')


@app.route('/jobs')
def job_list():
    """
    Display list of all jobs for employers.
    Shows jobs posted by the logged-in employer.
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to view jobs', 'error')
        return redirect(url_for('login'))
    
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get jobs for the logged-in employer
        cursor.execute(
            """SELECT j.*, e.company_name as employer_company
               FROM jobs j
               JOIN employers e ON j.employer_id = e.id
               WHERE j.employer_id = %s
               ORDER BY j.created_at DESC""",
            (session['user_id'],)
        )
        jobs = cursor.fetchall()
        cursor.close()
        
        return render_template('job_list.html', jobs=jobs)
        
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('job_list.html', jobs=[])


# ============================================
# Admin Dashboard Routes
# ============================================

@app.route('/admin/dashboard')
def admin_dashboard():
    """
    Admin dashboard to view and manage all job postings.
    Supports filtering by classification status.
    """
    # Check if user is logged in as admin
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash('Access denied. Admin login required.', 'error')
        return redirect(url_for('login'))
    
    # Get filter parameter
    filter_classification = request.args.get('filter', 'all')
    
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Build query based on filter
        # Explicitly select j.id to ensure it's available in the result
        if filter_classification == 'all':
            cursor.execute(
                """SELECT j.id, j.employer_id, j.company_name, j.email, j.job_title, j.salary, 
                          j.location, j.job_description, j.contact_details, j.detection_score, 
                          j.classification, j.created_at, j.updated_at,
                          e.username as employer_username, e.company_name as employer_company
                   FROM jobs j
                   JOIN employers e ON j.employer_id = e.id
                   ORDER BY j.created_at DESC"""
            )
        else:
            cursor.execute(
                """SELECT j.id, j.employer_id, j.company_name, j.email, j.job_title, j.salary, 
                          j.location, j.job_description, j.contact_details, j.detection_score, 
                          j.classification, j.created_at, j.updated_at,
                          e.username as employer_username, e.company_name as employer_company
                   FROM jobs j
                   JOIN employers e ON j.employer_id = e.id
                   WHERE j.classification = %s
                   ORDER BY j.created_at DESC""",
                (filter_classification,)
            )
        
        jobs = cursor.fetchall()
        
        # Get statistics
        cursor.execute(
            "SELECT classification, COUNT(*) as count FROM jobs GROUP BY classification"
        )
        stats = cursor.fetchall()
        stats_dict = {stat['classification']: stat['count'] for stat in stats}
        
        cursor.close()
        
        return render_template('admin_dashboard.html', 
                             jobs=jobs, 
                             filter_classification=filter_classification,
                             stats=stats_dict)
        
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('admin_dashboard.html', jobs=[], stats={})


@app.route('/admin/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    """
    Delete a job posting (admin only).
    Supports both regular form submission and AJAX requests.
    """
    # Check if user is logged in as admin
    if 'user_id' not in session or session.get('user_type') != 'admin':
        if request.is_json:
            return jsonify({'success': False, 'message': 'Access denied'}), 403
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Delete job
        cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
        db.commit()
        cursor.close()
        
        flash('Job deleted successfully', 'success')
        if request.is_json:
            return jsonify({'success': True, 'message': 'Job deleted successfully'})
        
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        if request.is_json:
            return jsonify({'success': False, 'message': 'Database error occurred'}), 500
        return redirect(url_for('admin_dashboard'))


# ============================================
# Application Initialization
# ============================================

if __name__ == '__main__':
    # Initialize database on first run
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        print("Make sure MySQL is running and database credentials are correct.")
    
    # Run Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
