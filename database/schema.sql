-- ============================================
-- Fake Job Detection System - Database Schema
-- ============================================
-- This file contains the MySQL database schema for the Fake Job Detection System
-- Run this script to create all necessary tables

-- Create database (uncomment if needed)
-- CREATE DATABASE IF NOT EXISTS fake_job_detection;
-- USE fake_job_detection;

-- ============================================
-- Table: employers
-- Stores employer account information
-- ============================================
CREATE TABLE IF NOT EXISTS employers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: admins
-- Stores administrator account information
-- ============================================
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: jobs
-- Stores job postings with detection scores and classifications
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    salary DECIMAL(10, 2),
    location VARCHAR(255),
    job_description TEXT NOT NULL,
    contact_details TEXT,
    -- Detection scoring fields
    detection_score INT DEFAULT 0,
    classification ENUM('Genuine', 'Suspicious', 'Fake') DEFAULT 'Genuine',
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Foreign key relationship
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE,
    -- Indexes for efficient querying
    INDEX idx_employer_id (employer_id),
    INDEX idx_classification (classification),
    INDEX idx_detection_score (detection_score),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Admin Account Creation
-- ============================================
-- To create an admin account, use the create_admin.py script:
--   python create_admin.py
-- 
-- Or manually insert with a properly hashed password:
--   INSERT INTO admins (username, email, password_hash) 
--   VALUES ('admin', 'admin@example.com', '<hashed_password>');
-- 
-- Use Python to generate password hash:
--   from werkzeug.security import generate_password_hash
--   hash = generate_password_hash('your_password')
