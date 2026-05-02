# Fake Job Detection System

A production-ready full-stack web application for detecting potentially fraudulent job postings using rule-based scoring algorithms. The system distinguishes between genuine, suspicious, and fake job listings and provides separate interfaces for employers and administrators.

## Features

- **Employer Portal**
  - User registration and authentication
  - Post job listings with automatic fraud detection
  - View all posted jobs with classification status
  - Real-time scoring and classification

- **Admin Dashboard**
  - View all job postings across the platform
  - Filter jobs by classification (Genuine, Suspicious, Fake)
  - Delete job postings
  - Statistics dashboard with classification counts

- **Rule-Based Detection System**
  - Gmail/Yahoo email addresses: +2 points
  - Salary exceeding $100,000: +2 points
  - Job description contains "fee", "registration", or "urgent hiring": +3 points
  - Empty location field: +1 point
  - Classification thresholds:
    - 0-2 points: Genuine
    - 3-5 points: Suspicious
    - 6+ points: Fake

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Password hashing with Werkzeug

## Project Structure

```
Fake Job Detection/
├── app.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── config/
│   └── database.py        # Database configuration
├── database/
│   └── schema.sql         # MySQL database schema
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── post_job.html
│   ├── job_list.html
│   └── admin_dashboard.html
└── static/
    ├── css/
    │   └── style.css      # Modern CSS styling
    └── js/
        └── main.js        # Frontend JavaScript
```

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)

2. **MySQL Server**
   - Download from [mysql.com](https://dev.mysql.com/downloads/mysql/)
   - Or use XAMPP/WAMP which includes MySQL

3. **pip** (Python package manager)
   - Usually comes with Python installation

## Installation & Setup

### Step 1: Clone or Download the Project

Navigate to your project directory:
```bash
cd "c:\Users\Lenovo\OneDrive\Desktop\Fake Job Detection"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

1. **Start MySQL Server**
   - If using XAMPP/WAMP, start MySQL from the control panel
   - If using standalone MySQL, ensure the service is running

2. **Create Database**
   - Open MySQL command line or phpMyAdmin
   - Create a new database (or the application will create it automatically):
   ```sql
   CREATE DATABASE fake_job_detection;
   ```

3. **Configure Database Connection**
   - Open `config/database.py`
   - Update the `DB_CONFIG` dictionary with your MySQL credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',           # Your MySQL username
       'password': 'your_password',  # Your MySQL password
       'database': 'fake_job_detection',
       ...
   }
   ```

### Step 5: Initialize Database Schema

The application will automatically create tables on first run, but you can also manually run the schema:

```bash
# Option 1: Let the app create tables automatically (recommended)
# Just run the app and it will initialize the database

# Option 2: Manual initialization
mysql -u root -p fake_job_detection < database/schema.sql
```

### Step 6: Create Admin Account

The schema includes a placeholder admin account. For production, you should:

1. Register through the application interface, OR
2. Manually insert an admin account with a properly hashed password

To create an admin account manually:
```python
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash('your_admin_password')
# Then insert into admins table
```

### Step 7: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage Guide

### For Employers

1. **Register an Account**
   - Navigate to `/register`
   - Fill in username, email, company name, and password
   - Click "Register"

2. **Login**
   - Navigate to `/login`
   - Select "Employer" account type
   - Enter credentials and login

3. **Post a Job**
   - Click "Post Job" in navigation
   - Fill in all required fields:
     - Company Name
     - Email
     - Job Title
     - Salary (optional)
     - Location (optional)
     - Job Description
     - Contact Details (optional)
   - Submit the form
   - The system will automatically calculate a fraud detection score and classify the job

4. **View Your Jobs**
   - Click "My Jobs" in navigation
   - View all your posted jobs with their classification status

### For Administrators

1. **Login**
   - Navigate to `/login`
   - Select "Admin" account type
   - Enter admin credentials

2. **Dashboard**
   - View statistics (Genuine, Suspicious, Fake job counts)
   - Filter jobs by classification using filter buttons
   - View detailed job information in the table

3. **Manage Jobs**
   - Click "Delete" button to remove any job posting
   - Confirm deletion in the popup dialog

## Default Admin Credentials

**Note**: The default admin account in the schema is a placeholder. You need to create a proper admin account with a hashed password.

To create an admin account:
1. Use the registration endpoint (modify it to allow admin registration), OR
2. Manually insert an admin with a hashed password using Python:
   ```python
   from werkzeug.security import generate_password_hash
   hash = generate_password_hash('your_password')
   # Insert into database
   ```

## Configuration

### Changing Secret Key

For production, change the secret key in `app.py`:
```python
app.secret_key = 'your-unique-secret-key-here'
```

### Database Configuration

Modify `config/database.py` to change database connection settings.

### Detection Rules

Modify the `calculate_fake_score()` function in `app.py` to adjust detection rules and thresholds.

## Troubleshooting

### Database Connection Errors

- **Error**: "Error connecting to MySQL"
  - **Solution**: Ensure MySQL server is running
  - Check database credentials in `config/database.py`
  - Verify MySQL user has proper permissions

### Port Already in Use

- **Error**: "Address already in use"
  - **Solution**: Change the port in `app.py`:
    ```python
    app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
    ```

### Module Not Found Errors

- **Error**: "No module named 'flask'"
  - **Solution**: Ensure virtual environment is activated and dependencies are installed:
    ```bash
    pip install -r requirements.txt
    ```

### Table Creation Errors

- **Error**: "Table already exists"
  - **Solution**: Drop existing tables or use a fresh database

## Security Considerations

1. **Change Secret Key**: Update `app.secret_key` in production
2. **Use Environment Variables**: Store database credentials in environment variables
3. **HTTPS**: Use HTTPS in production
4. **Password Hashing**: Already implemented using Werkzeug
5. **SQL Injection**: Using parameterized queries (already implemented)
6. **Input Validation**: Client and server-side validation implemented

## Development

### Adding New Detection Rules

Edit the `calculate_fake_score()` function in `app.py`:

```python
def calculate_fake_score(job_data):
    score = 0
    # Add your new rule here
    # if condition:
    #     score += points
    ...
```

### Customizing UI

- **CSS**: Modify `static/css/style.css`
- **JavaScript**: Modify `static/js/main.js`
- **Templates**: Edit files in `templates/` directory

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in the console
3. Verify all prerequisites are installed correctly

## Future Enhancements

Potential improvements:
- Machine learning-based detection
- Email notifications
- Job posting analytics
- Export functionality
- Advanced filtering options
- User profile management
- Job editing capabilities

---

**Built with Flask and MySQL** | **Version 1.0**
