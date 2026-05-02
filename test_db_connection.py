"""
Database Connection Test Script
================================
This script tests the MySQL database connection and initializes the database schema.
Run this script to verify your database setup before running the Flask application.

Usage:
    python test_db_connection.py
"""

import mysql.connector
from mysql.connector import Error
from config.database import DB_CONFIG, init_db

def test_connection():
    """Test basic MySQL connection"""
    print("=" * 60)
    print("Testing MySQL Database Connection")
    print("=" * 60)
    print(f"\nConnection Settings:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  Password: {'*' * len(DB_CONFIG['password']) if DB_CONFIG['password'] else '(empty)'}")
    print("\n" + "-" * 60)
    
    try:
        # Test connection without database first
        config_test = {
            'host': DB_CONFIG['host'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password']
        }
        
        print("\nStep 1: Testing MySQL server connection...")
        conn = mysql.connector.connect(**config_test)
        
        if conn.is_connected():
            print("[OK] MySQL server connection successful!")
            
            # Get MySQL version
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"[OK] MySQL Version: {version[0]}")
            cursor.close()
            conn.close()
        else:
            print("[ERROR] Failed to connect to MySQL server")
            return False
            
    except Error as e:
        print(f"[ERROR] Error connecting to MySQL server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check if username and password are correct in config/database.py")
        print("3. Verify MySQL is installed and accessible")
        return False
    
    # Test database connection
    try:
        print("\nStep 2: Testing database connection...")
        conn = mysql.connector.connect(**DB_CONFIG)
        
        if conn.is_connected():
            print(f"[OK] Successfully connected to database '{DB_CONFIG['database']}'!")
            
            # Check if tables exist
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n[OK] Found {len(tables)} existing table(s):")
                for table in tables:
                    print(f"    - {table[0]}")
            else:
                print("\n[WARNING] No tables found. Database needs to be initialized.")
            
            cursor.close()
            conn.close()
            return True
            
    except Error as e:
        if "Unknown database" in str(e):
            print(f"[WARNING] Database '{DB_CONFIG['database']}' does not exist yet.")
            print("   It will be created during initialization.")
        else:
            print(f"[ERROR] Error connecting to database: {e}")
            return False
    
    return True


def initialize_database():
    """Initialize database schema"""
    print("\n" + "=" * 60)
    print("Initializing Database Schema")
    print("=" * 60)
    
    try:
        init_db()
        print("\n[OK] Database initialization completed successfully!")
        return True
    except Exception as e:
        print(f"\n[ERROR] Error initializing database: {e}")
        print("\nTroubleshooting:")
        print("1. Check if you have CREATE DATABASE privileges")
        print("2. Verify the schema.sql file exists and is readable")
        print("3. Check MySQL error logs for more details")
        return False


def main():
    """Main function to test and initialize database"""
    print("\n")
    
    # Test connection
    if not test_connection():
        print("\n" + "=" * 60)
        print("[ERROR] Connection test failed. Please fix the issues above.")
        print("=" * 60)
        print("\nTo fix this:")
        print("1. Open config/database.py")
        print("2. Update the 'password' field with your MySQL root password")
        print("3. If you don't have a password, set it to: '' (empty string)")
        print("4. If using XAMPP/WAMP, the default password is usually empty")
        print("5. Run this script again: python test_db_connection.py")
        return
    
    # Ask if user wants to initialize
    print("\n" + "-" * 60)
    response = input("\nDo you want to initialize/create the database schema? (y/n): ").strip().lower()
    
    if response == 'y' or response == 'yes':
        if initialize_database():
            print("\n" + "=" * 60)
            print("[OK] Database setup completed successfully!")
            print("=" * 60)
            print("\nYou can now run the Flask application:")
            print("  python app.py")
        else:
            print("\n" + "=" * 60)
            print("[ERROR] Database initialization failed.")
            print("=" * 60)
    else:
        print("\nSkipping database initialization.")
        print("The database will be initialized automatically when you run app.py")
    
    print("\n")


if __name__ == '__main__':
    main()
