"""
Admin Account Creation Script
==============================
This script helps create an admin account with a properly hashed password.
Run this script after setting up the database to create your admin account.

Usage:
    python create_admin.py
    python create_admin.py --username ebshibha --email ebshibha@admin.local --password ammu
"""

from werkzeug.security import generate_password_hash
from config.database import DB_CONFIG
import mysql.connector
from mysql.connector import Error
import argparse

def create_admin_account():
    """Create an admin account (interactive or via flags)."""
    parser = argparse.ArgumentParser(description="Create an admin account in the Fake Job Detection database.")
    parser.add_argument("--username", type=str, help="Admin username")
    parser.add_argument("--email", type=str, help="Admin email")
    parser.add_argument("--password", type=str, help="Admin password (will be hashed)")
    args = parser.parse_args()

    print("=" * 50)
    print("Admin Account Creation")
    print("=" * 50)

    # Get admin details (flags take precedence; otherwise prompt)
    username = (args.username or input("Enter admin username: ")).strip()
    email = (args.email or input("Enter admin email: ")).strip()
    password = (args.password or input("Enter admin password: ")).strip()
    
    if not all([username, email, password]):
        print("Error: All fields are required!")
        return

    # Keep login compatible with any password length; warn only.
    if len(password) < 6:
        print("Warning: Using a short password (< 6 characters). This is not recommended.")
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute(
            "SELECT id FROM admins WHERE username = %s OR email = %s",
            (username, email)
        )
        if cursor.fetchone():
            print("Error: Username or email already exists!")
            cursor.close()
            conn.close()
            return
        
        # Insert admin account
        cursor.execute(
            """INSERT INTO admins (username, email, password_hash)
               VALUES (%s, %s, %s)""",
            (username, email, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✓ Admin account created successfully!")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print("\nYou can now login with these credentials.")
        
    except Error as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. MySQL server is running")
        print("2. Database credentials in config/database.py are correct")
        print("3. Database 'fake_job_detection' exists")

if __name__ == '__main__':
    create_admin_account()
