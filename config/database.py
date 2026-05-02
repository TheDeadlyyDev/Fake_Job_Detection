"""
Database Configuration Module
==============================
This module handles database connection configuration for MySQL.
Modify the connection parameters according to your MySQL setup.
"""

import os
import mysql.connector
from mysql.connector import Error
from flask import g

# Database configuration parameters
DB_CONFIG = {
    # Supports environment overrides so credentials aren't hardcoded in code.
    # Common XAMPP/WAMP default: user=root, password=(empty)
    'host': os.environ.get('FAKEJOB_DB_HOST', 'localhost'),
    'user': os.environ.get('FAKEJOB_DB_USER', 'root'),
    # Default updated to match your local MySQL Workbench connection.
    'password': os.environ.get('FAKEJOB_DB_PASSWORD', 'ammu8610@'),
    'database': os.environ.get('FAKEJOB_DB_NAME', 'fake_job_detection'),
    'port': int(os.environ.get('FAKEJOB_DB_PORT', '3307')),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
}


def get_db():
    """
    Get database connection using Flask's application context.
    Creates a new connection if one doesn't exist for the current request.
    
    Returns:
        mysql.connector.connection: MySQL database connection object
    """
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**DB_CONFIG)
            if g.db.is_connected():
                print("Database connection successful")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    
    return g.db


def close_db(e=None):
    """
    Close database connection at the end of request.
    This function is registered as a teardown handler in Flask.
    
    Args:
        e: Exception object if an error occurred during request
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()
        print("Database connection closed")


def init_db():
    """
    Initialize database by reading and executing schema.sql file.
    This function creates all necessary tables if they don't exist.
    """
    try:
        # Read schema file
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Connect to MySQL server (without database first)
        config_without_db = DB_CONFIG.copy()
        database_name = config_without_db.pop('database')
        
        conn = mysql.connector.connect(**config_without_db)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")
        
        # Execute schema SQL (split by semicolon for multiple statements)
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Error as e:
                    print(f"Warning: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully")
        
    except Error as e:
        print(f"Error initializing database: {e}")
        raise
