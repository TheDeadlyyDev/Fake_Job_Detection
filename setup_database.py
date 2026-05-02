"""
Database Setup Helper Script
=============================
Interactive script to configure database connection settings.
This will help you set up your MySQL credentials.

Usage:
    python setup_database.py
"""

import os
import re

def update_database_config():
    """Update database configuration interactively"""
    print("=" * 60)
    print("Database Configuration Setup")
    print("=" * 60)
    print("\nThis script will help you configure MySQL database connection.")
    print("\nCommon MySQL setups:")
    print("  - XAMPP/WAMP: Usually password is empty (just press Enter)")
    print("  - Standalone MySQL: Use your MySQL root password")
    print("  - MySQL Workbench: Check your connection settings")
    print("\n" + "-" * 60)
    
    # Get current config values
    config_file = 'config/database.py'
    
    # Read current config
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[ERROR] Config file not found: {config_file}")
        return False
    
    # Get user input
    print("\nEnter MySQL connection details:")
    print("(Press Enter to keep current value)")
    
    # Host
    current_host = re.search(r"'host':\s*'([^']+)'", content)
    current_host = current_host.group(1) if current_host else 'localhost'
    host = input(f"\nMySQL Host [{current_host}]: ").strip() or current_host
    
    # User
    current_user = re.search(r"'user':\s*'([^']+)'", content)
    current_user = current_user.group(1) if current_user else 'root'
    user = input(f"MySQL Username [{current_user}]: ").strip() or current_user
    
    # Password
    current_password = re.search(r"'password':\s*'([^']*)'", content)
    current_password = current_password.group(1) if current_password else ''
    password = input(f"MySQL Password [{'*' * len(current_password) if current_password else '(empty)'}]: ").strip()
    if not password:
        password = current_password  # Keep current if empty
    
    # Database name
    current_db = re.search(r"'database':\s*'([^']+)'", content)
    current_db = current_db.group(1) if current_db else 'fake_job_detection'
    database = input(f"Database Name [{current_db}]: ").strip() or current_db
    
    # Update config file
    updated_content = content
    
    # Replace host
    updated_content = re.sub(
        r"'host':\s*'[^']+'",
        f"'host': '{host}'",
        updated_content
    )
    
    # Replace user
    updated_content = re.sub(
        r"'user':\s*'[^']+'",
        f"'user': '{user}'",
        updated_content
    )
    
    # Replace password (handle empty string)
    updated_content = re.sub(
        r"'password':\s*'[^']*'",
        f"'password': '{password}'",
        updated_content
    )
    
    # Replace database
    updated_content = re.sub(
        r"'database':\s*'[^']+'",
        f"'database': '{database}'",
        updated_content
    )
    
    # Write updated config
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("\n" + "=" * 60)
        print("[OK] Database configuration updated successfully!")
        print("=" * 60)
        print(f"\nUpdated settings:")
        print(f"  Host: {host}")
        print(f"  User: {user}")
        print(f"  Password: {'*' * len(password) if password else '(empty)'}")
        print(f"  Database: {database}")
        print("\nNow you can test the connection:")
        print("  python test_db_connection.py")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed to update config file: {e}")
        return False


def main():
    """Main function"""
    try:
        update_database_config()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")


if __name__ == '__main__':
    main()
