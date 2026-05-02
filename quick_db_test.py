"""
Quick Database Connection Test
==============================
Tests database connection with common password scenarios.
"""

import mysql.connector
from mysql.connector import Error

def test_connection_with_password(password):
    """Test connection with a specific password"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )
        if conn.is_connected():
            print(f"[SUCCESS] Connected with password: {'(empty)' if not password else '***'}")
            conn.close()
            return True
    except Error as e:
        return False
    return False

def main():
    """Test common password scenarios"""
    print("=" * 60)
    print("Quick Database Connection Test")
    print("=" * 60)
    print("\nTesting common MySQL password scenarios...\n")
    
    # Common passwords to try
    passwords_to_try = ['', 'root', 'password', 'admin', '123456']
    
    success = False
    for pwd in passwords_to_try:
        if test_connection_with_password(pwd):
            print(f"\n[INFO] Working password found!")
            print(f"[INFO] Update config/database.py line 16 with:")
            if not pwd:
                print(f"        'password': '',")
            else:
                print(f"        'password': '{pwd}',")
            success = True
            break
    
    if not success:
        print("\n[ERROR] None of the common passwords worked.")
        print("\nPlease:")
        print("1. Check your MySQL password")
        print("2. Update config/database.py manually")
        print("3. Or run: python setup_database.py")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
